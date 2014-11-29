from enum import IntEnum, unique
from PySide import QtGui, QtCore

class AbstractDataFields(IntEnum):
    """
    The AbstractDataFields class provides an enumeration of the various fields within a DataModel.
    """
    @classmethod
    def fields(cls):
        """
        Generates a list of enum variables in this class.

        @returns A list class attributes that act as the enum values
        """
        return [e.name for e in cls]

    @classmethod
    def fieldvalues(cls):
        """
        Generates a list of enum variables in this class.

        @returns A list class attributes that act as the enum values
        """
        return [e.value for e in cls]

    @classmethod
    def headerdata(cls):
        """
        Generates an AbstractData containing header data for SceneGraphType

        @returns An AbstractData object with header data.
        """
        return AbstractData.BuildData(dict((getattr(cls, field), field.capitalize()) for field in cls.fields()))

    @classmethod
    def size(cls):
        """
        Calculates the size of the fields list.

        @returns The size of the field list.
        """
        return len(cls.fields())

class AbstractData(QtCore.QObject):
    """
    The AbstractData class is a structure to map static data to the various QtCore.Qt.ItemDataRole value.  It's goal is to provide easy access when used in conjuction with a AbtractItemModel's data() and setData() method.

    Internally the data is a dimentional dictionary, structured as:
        Data {
            <ItemDataRole Key 0> :
            {
                <Column Key 0> : <Column 0 Data>,
                <Column Key 1> : <Column 1 Data>,
                <Column Key 2> : <Column 2 Data>
                ...
                <Column Key N> : <Column N Data>
            }
            <ItemDataRole Key 1> :
            {
                <Column Key 0> : <Column 0 Data>,
                <Column Key 1> : <Column 1 Data>,
                <Column Key 2> : <Column 2 Data>
                ...
                <Column Key N> : <Column N Data>
            }
            ...
            <ItemDataRole Key N> :
            {
                <Column Key 0> : <Column 0 Data>,
                <Column Key 1> : <Column 1 Data>,
                <Column Key 2> : <Column 2 Data>
                ...
                <Column Key N> : <Column N Data>
            }
        }

    So that usage is as follows

        value = data[<ItemDataRole Key>, <Column Key>]

    or

        data[<ItemDataRole Key>, <Column Key>] = value

    The list of values for the Qt Item Data Role can be found here http://qt-project.org/doc/qt-4.8/qt.html#ItemDataRole-enum
    """
    # Extends the ItemDataRole
    FlagRole = int(QtCore.Qt.UserRole) + 1

    def __init__(self, sdata=None, parent=None):
        """
        Constructor

        @param sdata An initial dictionary of static data
        @param parent The QObject parent object.
        """
        super(AbstractData, self).__init__(parent)
        self._internal = sdata if sdata else {}

    def __len__(self):
        """
        Return the length (the number of items) the data.
        """
        # Use QtCore.Qt.DisplayRole as our column data role.
        return len(self._internal.get(QtCore.Qt.DisplayRole, {}))

    def __getitem__(self, ids):
        """
        The [] operator getter.  This is specialized to take a tuple (<ItemDataRole Key>, <Column Key>).

        Example:

            value = data[<ItemDataRole Key>, <Column Key>]

        @param ids The lookup key consisting of (<ItemDataRole Key>, <Column Key>).
        @returns The value associated with the ids, if the ids are valid; None otheriwse
        """
        if len(ids) != 2:
            raise ValueError("'ids' parameter must be a 2 dimensional tuple.")

        return self.get(ids[0], ids[1])

    def __setitem__(self, ids, value):
        """
        The [] operator setter.  This is specialized to take a tuple (<ItemDataRole Key>, <Column Key>).

        Example:

            data[<ItemDataRole Key>, <Column Key>] = value

        @param ids The lookup key consisting of (<ItemDataRole Key>, <Column Key>).
        @param value The value to associate with the ids, replaing any existing value.
        """
        if len(ids) != 2:
            raise ValueError("'ids' parameter must be a 2 dimensional tuple.")

        self.set(ids[0], ids[1], value)

    def get(self, role, column, default=None):
        """
        Gets the data stored with the specific role and column.

        @param role    A QtCore.Qt.ItemDataRole dictionary key associated with the data
        @param column  A column dictionary key associated with the data
        @param default The value to return if no key exists.
        @returns        The value associated with the role and column keys, if the ids are valid; None otheriwse
        """
        columndata = self._internal.get(role, None)
        return columndata.get(column, default) if columndata else default

    def set(self, role, column, value):
        """
        Sets the data stored with the specific role and column.

        @param role    A QtCore.Qt.ItemDataRole dictionary key associated with the data
        @param column  A column dictionary key associated with the data
        @param value   The data to associate with the ItemDataRole and Column keys
        @returns        The value associated with the role and column keys, if the ids are valid; None otheriwse
        """
        # Create the Column Data if it is not already created
        columndata = self._internal.setdefault(role, {})
        columndata[column] = value

    def data(self, role=QtCore.Qt.DisplayRole):
        """
        Retrieve the data stored with the specific role.

        @param role An value of QtCore.Qt.ItemDataRole enum.

        """
        return self._internal.get(role, {})

    @staticmethod
    def BuildData(rawdata, roles=[QtCore.Qt.ToolTipRole, QtCore.Qt.AccessibleTextRole, QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]):
        """
        Constructs an AbstractData instance from a iterable of data and a list of roles.
        @param rawdata An iterable collectio of data
        @param roles   A list of ItemDataRole values.
        @returns        A valid AbstractData() if possible; None otherwise.
        """
        columndata = None
        if isinstance(rawdata, list):
            columndata = dict((i, rawdata[i]) for i in range(len(rawdata)))
        if isinstance(rawdata, dict):
            columndata = rawdata

        data = AbstractData()
        if columndata:
            for key in columndata:
                for role in roles:
                    data[role, key] = columndata[key]
            return data

        return data

class AbstractDataItem(QtCore.QObject):
    """
    The Data Item class provides a collection of static and virtual data to be used as a entry in a data model.

    Static data is an instance of AbstractData and is cached locally.

    Virtual data is managed by overloading the data() and setData() method of the model.
    """
    dataChanging = QtCore.Signal(object, object)
    dataChanged  = QtCore.Signal(object, object)

    def __init__(self, sdata=AbstractData(), parent = None):
        """
        Constructor

        @param sdata The initial instance of AbstractData

        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial parent object of this AbstractDataItem
        """
        super(AbstractDataItem, self).__init__(parent)
        self._staticdata = sdata if isinstance(sdata, AbstractData) else AbstractData.BuildData(sdata)

    def __getitem__(self, id):
        """
        The [] operator getter.

        @param id The lookup key to the data.
        @exception IndexError if no data is associated with the id.
        """
        if not self.hasData(id):
            raise IndexError()
        return self.data(id)

    def __setitem__(self, id, item):
        """
        The [] operator setter.
        @param id The lookup ke to the data
        @param item The data to associate with the id.
        """
        return self.setData(id, item)

    def _dataChanging(self, index, role):
        """
        Internal method to emit the dataChanging signal.

        @param index The index of the data.
        @param role  The data role of the data.
        """
        self.dataChanging.emit(index, role)

    def _dataChanged(self, index, role):
        """
        Internal method to emit the dataChanged signal.

        @param index The index of the data.
        @param role  The data role of the data.
        """
        self.dataChanged.emit(index, role)

    def row(self):
        """
        Returns the row component of the QModelIndex of this item within the parent's child collection

        @returns The respective index if parent is valid; -1 otherwise.
        """
        if self.parent():
            index = self.parent().itemIndex(self)
            if index and index.isValid():
                return index.row()

        return -1

    def size(self):
        """
        Returns number of data stored at this item.

        @returns The length of the internal collection.
        """
        return len(self._staticdata)

    def dataIndex(self, data, role=QtCore.Qt.DisplayRole):
        """
        Returns the id of data stored at this item.

        @returns A valid id if found; -1 otherwise.
        """
        for i in range(self.size()):
            if self.data(i, role) == data:
                return i

        return -1

    def data(self, id, role=QtCore.Qt.DisplayRole):
        """
        Gets the data for the corresponding id, filtered by the given role.

        @param id The lookup key to the data.
        @param role The filter key of the lookup operation.
        @returns The data if the lookup operation was succesful; False otherwise.
        """
        return self._staticdata[role, id]

    def setData(self, id, value, role=QtCore.Qt.EditRole):
        """
        Sets the data for the corresponding id, filtered by the given role.

        @param id The lookup key to the data.
        @param role The filter key of the data storing operation.
        @returns True is operation was succesful; False otherwise.
        """
        self._dataChanging(id, role)
        self._staticdata[role, id] = value
        self._dataChanged(id, role)

        return True

    def hasData(self, id, role=QtCore.Qt.DisplayRole):
        """
        Queries if data exists for the id, role combination.

        @param id The lookup key to the data.
        @param role The filter key of the lookup operation.
        @returns True if data exists; False otherwise.
        """
        return self._staticdata[role, id] != None

    def flags(self, id):
        """
        Get the Qt.ItemFlags for the model data at a given id.

        @param id The lookup key to the data.
        @returns A valid combination of the QtCore.Qt.QFlags enum.
        """
        return self.data(id, AbstractData.FlagRole) or (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def setFlags(self, id, value):
        """
        Set the Qt.ItemFlags for the model data at a given id.

        @param id    The lookup key to the data.
        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        self.setData(id, value, AbstractData.FlagRole)

    def insertFlags(self, value):
        """
        Adds the Qt.ItemFlags to the model data for all data.

        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        for id in self._staticdata.data(AbstractData.FlagRole):
            self.setFlags(id, self.flags(id) | value)

    def removeFlags(self, value):
        """
        Removes the Qt.ItemFlags from the model data for all data.

        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        for id in self._staticdata.data(AbstractData.FlagRole):
            self.setFlags(id, self.flags(id) & ~value)

class AbstractDataTreeItem(AbstractDataItem):
    """
    The Data Tree Item class provides extends the Data Item class with tree relationships between itself and Data Tree Items.
    """
    childAdded    = QtCore.Signal(object)
    childRemoved  = QtCore.Signal(object)

    def __init__(self, sdata, parent=None):
        """
        Constructor.

        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial parent AbstractDataTreeItem of this AbstractDataTreeItem
        """
        super(AbstractDataTreeItem, self).__init__(sdata, parent)
        self._children = []

    def _childAdded(self, item):
        """
        Internal method to emit the childAdded signal.

        @parem item The item that has been added as a 'child'
        """
        self.childAdded.emit(item)

    def _childRemoved(self, item):
        """
        Internal method to emit the childRemoved signal.

        @parem item The item that has been removed as a 'child'
        """
        self.childRemoved.emit(item)

    def isRoot(self):
        """
        Queries the node if it is a root node.

        @returns True if the item is a root item; False otherwise.
        """
        return not bool(self.parent())

    def row(self):
        """
        Returns the row component of the QModelIndex of this item within the parent's child collection

        @returns The respective index if parent is valid; -1 otherwise.
        """
        if self.parent():
            return self.parent().childPosition(self)

        return 0

    def column(self):
        """
        Returns the column component of the QModelIndex of this item within the parent's child collection

        @returns The respective index if parent is valid; 0 otherwise.
        """
        return 0

    def appendChild(self, item):
        """
        Appends a child item to internal collection of children.

        @param item the item to append.
        """
        self._children.append(item)
        self._childAdded(item)

    def insertChild(self, position, item):
        """
        Inserts a child item into the internal collection of children.

        @param item the item to insert
        @param position the position to insert the item.
        """
        self._children.insert(position, item)
        self._childAdded(item)

    def removeChild(self, item):
        """
        Removes a item from the children list.

        @param item the item to remove
        """
        return self.removePosition(self.childPosition(item))

    def removePosition(self, position):
        """
        Removes a item from the children list at a specific position.

        @param position The position to remove.
        """
        child = self._children.pop(position)
        self._childRemoved(child)
        return child

    def child(self, position):
        """
        Returns the child AbstractDataTreeItem at the given position.

        @param position The position into the list of children.
        @returns The respective item if row is valid; None otherwise
        """
        return self._children[position] if position >= 0 and position < len(self._children) else None

    def hasChildren(self):
        """
        Returns the state of children collection.

        @returns True if the item has children; False otherwise.
        """
        return bool(self._children)

    def childCount(self):
        """
        Returns number of children stored at this item.

        @returns The number of children at this item.
        """
        return len(self._children)

    def childPosition(self, child):
        """
        Returns the position of the given child AbstractDataTreeItem in the internal children list

        @param child The child to query.
        @returns A valid index if the child is in the internal children list; None otherwise.
        """
        return self._children.index(child)

    def rowCount(self):
        """
        Returns number of rows stored at this item.

        @returns The number of rows at this item.
        """
        return len(self._children)

    def columnCount(self):
        """
        Returns number of columns stored at this item.

        @returns The number of columns at this item.
        @warning This method is used indirectly by the model to request data; the value returned must match the total of static and virtual data.
        """
        return self.size()

    def insertFlags(self, value):
        """
        Adds the Qt.ItemFlags to the model data for all data.

        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        super(AbstractDataTreeItem, self).insertFlags(value)

        for child in self._children:
            child.insertFlags(value)

    def removeFlags(self, value):
        """
        Removes the Qt.ItemFlags from the model data for all data.

        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        super(AbstractDataTreeItem, self).removeFlags(value)

        for child in self._children:
            child.removeFlags(value)

class AbstractDataListModel(QtCore.QAbstractListModel):
    """
    The Data List model provides a List Data Item model implementation of a QAbstractListModel.
    """
    def __init__(self, parent=None):
        """
        Constructor

        @param parent The QObject parent object.
        """
        super(AbstractDataListModel, self).__init__(parent)

        self._items = []
        self._flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def _dataChanging(self, topLeft, bottomRight=None):
        """
        Internal method to emit the dataChanging signal.

        @param topLeft     The top and left most QtCore.QModelIndex of the data.
        @param bottomRight The bottom and right most QtCore.QModelIndex of the data.
        """
        #self.dataChanging.emit(topLeft, bottomRight or topLeft)

    def _dataChanged(self, topLeft, bottomRight=None):
        """
        Internal method to emit the dataChanged signal.

        @param topLeft     The top and left most QtCore.QModelIndex of the data.
        @param bottomRight The bottom and right most QtCore.QModelIndex of the data.
        """
        self.dataChanged.emit(topLeft, bottomRight or topLeft)

    def _itemInsert(self, item):
        """
        Internal item insert.

        @param item  The item to append to end of the internal collection
        """
        self._items.append(item)
        self._itemConnect(item)

    def _itemInsertPosition(self, item, index):
        """
        Internal item insert.

        @param item  The item to append to end of the internal collection.
        @param index The internal index of the item in the internal collection.
        """
        self._items.insert(position, item)
        self._itemConnect(item)

    def _itemRemove(self, item):
        """
        Internal item removal.

        @param item  The item to remove from the internal collection.
        """
        try:
            self._items.remove(item)
            self._itemDisconnect(item)
        except ValueError:
            pass

    def _itemRemovePosition(self, index):
        """
        Internal item removal.

        @param index  The index of the item to remove from the internal collection.
        """
        try:
            item = self._items.pop(index)
            self._itemDisconnect(item)
        except IndexError:
            pass

    def _itemConnect(self, item):
        """
        Internal item signal connection.

        @param item  The item to connect to.
        """
        item.dataChanging.connect(self._itemChanging)
        item.dataChanged.connect(self._itemChanged)

    def _itemDisconnect(self, item):
        """
        Internal item signal disconnection.

        @param item  The item to disconnect from.
        """
        item.dataChanging.disconnect()
        item.dataChanged.disconnect()

    def _itemChanging(self, id, role):
        """
        Internal item changed event handler.
        """
        item = self.sender()
        index = self.createIndex(item.row(), id, item)
        self._dataChanging(index)

    def _itemChanged(self, id, role):
        """
        Internal item changed event handler.
        """
        item = self.sender()
        index = self.createIndex(item.row(), id, item)
        self._dataChanged(index)

    def createItem(self, *args):
        """
        Generates a new instance of the internal data item given the arguments.

        @param args The list of arguments to pass on the item.
        """
        return AbstractDataItem(*args)

    def columnCount(self, parent = QtCore.QModelIndex()):
        """
        Returns the number of columns in this model.
        """
        return 1

    def rowCount(self, parent = QtCore.QModelIndex()):
        """
        Returns the length of the item list.
        """
        return len(self._items)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        Returns the model data for the corresponding index, filtered by the given role.
        """
        item = self.item(index)
        return item.data(index.column(), role) if item else None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Sets the model data at a given index, filtered by the given role to the value.
        """
        item = self.item(index)
        return item.setData(index.column(), value, role) if item else False

    def flags(self, index):
        """
        Get the Qt.ItemFlags for the model data at a given index.

        @param index The lookup key to the data.
        @returns A valid combination of the QtCore.Qt.QFlags enum.
        """
        item = self.item(index)
        if item:
            return item.flags(index.column())
        return QtCore.Qt.ItemIsEnabled

    def setFlags(self, index, value):
        """
        Sets the Qt.ItemFlags for the model data at a given index.

        @param index The lookup key to the data.
        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        item = self.item(index)
        if item:
            item.setFlags(index, value)

    def insertFlags(self, value):
        """
        Adds the Qt.ItemFlags to the model data for all data.

        @param index The lookup key to the data.
        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        self._flags |= value
        for r in range(self.rowCount()):
            self._items[r].insertFlags(value)

    def removeFlags(self, value):
        """
        Removes the Qt.ItemFlags from the model data for all data.

        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        self._flags &= ~value
        for r in range(self.rowCount()):
            self._items[r].removeFlags(value)

    def headerData(self, section, orientation, role):
        """
        Returns the Header Data for this model
        """
        return None

    def index(self, row, column, parent = QtCore.QModelIndex()):
        """
        Returns the index of the internal data item in the model specified by the given row, column and parent index.

        @param   row The row index into the model
        @param   column The column index into the model
        @param   parent The optional parent QModelIndex
        @returns The QModelIndex of the lookup operation.
        @note    Required for QAbstractItemModel implementation
        """
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if self._items[row]:
            return self.createIndex(row, column,  self._items[row])
        else:
            return QtCore.QModelIndex()

    def item(self, index):
        """
        Returns the internal data item given the index

        @param index the QModelIndex representing the item
        @returns the respective item if the index is valid; None otherwise
        """
        if isinstance( index, ( int ) ):
            return self._items[index]

        if isinstance( index, ( QtCore.QModelIndex ) ) and index.isValid():
            item = index.internalPointer()
            if item:
                return item
            return self._items[index.row()]

        return None

    def itemIndex(self, item):
        """
        Returns the index for a given item

        @param A item already in the model.
        @returns The QModelIndex of the lookup operation.
        """
        for r in range(len(self._items)):
            if self._items[r] == item:
                return self.createIndex(r, 0, self._items[r])
            c = self._items[r].dataIndex(item)
            if c != -1:
                return self.createIndex(r, c, self._items[r])

        return QtCore.QModelIndex()

    def appendItem(self, item):
        """
        Appends an existing AbstractDataItem into the model.

        @returns The QModelIndex of the insert operation.
        """
        nextIndex = self.rowCount()
        lastIndex = nextIndex
        self.beginInsertRows(QtCore.QModelIndex(), nextIndex, lastIndex)

        self._itemInsert(item)

        self.endInsertRows()
        return self.itemIndex(item)

    def removeItem(self, item):
        """
        Remove an existing AbstractDataItem from the model.

        @returns True if the remove operation was succesful; False otherwise.
        """
        return self.removeRows(self.index(item).row())

    def insertRows(self, position, rows=1, index=QtCore.QModelIndex()):
        """
        Insert a rows with an empty DataItems into the model.

        @returns A list of respective QModelIndexes of the insert operation.
        """
        endIndex  = position + rows
        nextIndex = position
        lastIndex = endIndex - 1
        items = []
        self.beginInsertRows(QtCore.QModelIndex(), nextIndex, lastIndex)

        for row in range(nextIndex, endIndex):
            item = self.createItem()
            items.append(item)
            self._itemInsert(item, row)

        self.endInsertRows()
        return [self.itemIndex(item) for item in items]

    def removeRows(self, position, rows=1, index=QtCore.QModelIndex()):
        """
        Remove a row from the model.
        """
        endIndex  = position + rows
        nextIndex = position
        lastIndex = endIndex - 1
        self.beginRemoveRows(QtCore.QModelIndex(), nextIndex, lastIndex)

        # Reverse sort to iterate and delete at the same
        for i in sorted(range(nextIndex, endIndex), reverse=True):
            self._itemRemovePosition(i)

        self.endRemoveRows()
        return True

    def clear(self):
        """
        Clears the model of all data
        """
        self.removeRows(0, self.rowCount())

    def reload(self, *args):
        """
        Method to generate the internal data items.

        @param args Optional arguments that affects data generation.
        """
        raise NotImplementedError()

class AbstractDataTreeModel(QtCore.QAbstractItemModel):
    """
    The Data Tree model provides a Tree Data Item model implementation of a QAbstractItemModel.
    """
    def __init__(self, headerData=[], parent=None):
        """
        Constructor.

        @param headerdata The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent     The QObject parent object.
        """
        super(AbstractDataTreeModel, self).__init__(parent)

        self._root  = self.createRoot(headerData)
        self._flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def _dataChanging(self, topLeft, bottomRight=None):
        """
        Internal method to emit the dataChanging signal.

        @param topLeft     The top and left most QtCore.QModelIndex of the data.
        @param bottomRight The bottom and right most QtCore.QModelIndex of the data.
        """
        #self.dataChanging.emit(topLeft, bottomRight or topLeft)
        pass

    def _dataChanged(self, topLeft, bottomRight=None):
        """
        Internal method to emit the dataChanged signal.

        @param topLeft     The top and left most QtCore.QModelIndex of the data.
        @param bottomRight The bottom and right most QtCore.QModelIndex of the data.
        """
        self.dataChanged.emit(topLeft, bottomRight or topLeft)

    def _itemChanging(self, id, role):
        """
        Internal item changed event handler.
        """
        item = self.sender()
        index = self.createIndex(item.row(), id, item)
        self._dataChanging(index)

    def _itemChanged(self, id, role):
        """
        Internal item changed event handler.
        """
        item = self.sender()
        index = self.createIndex(item.row(), id, item)
        self._dataChanged(index)

    def _itemInsert(self, parent, item):
        """
        Internal item insert.

        @param parent The parent that will contain the item.
        @param item   The item to append to end of the parent's internal collection
        """
        parent.appendChild(item)
        item.setParent(parent)
        self._itemConnect(item)

    def _itemInsertPosition(self, parent, item, position):
        """
        Internal item insert.

        @param parent    The parent item that will contain the new item in its internal collection.
        @param item      The item to insert into the parent's internal collection.
        @param position  The position where the insertion operation will take place in the parent's internal collection
        """
        parent.insertChild(position, item)
        item.setParent(parent)
        self._itemConnect(item)

    def _itemRemove(self, parent, item):
        """
        Internal item removal.

        @param parent    The parent item that contains the item in its internal collection.
        @param item      The item to remove from the parent's internal collection.
        """
        try:
            parent.removeChild(item)
            item.setParent(None)
            self._itemDisconnect(item)
        except ValueError:
            pass

    def _itemRemovePosition(self, parent, position):
        """
        Internal item removal.

        @param parent    The parent item that contains the item in its internal collection.
        @param position  The position to remove from the parent's internal collection.
        """
        try:
            item = parent.removePosition(position)
            item.setParent(None)
            self._itemDisconnect(item)
        except IndexError:
            pass

    def _itemConnect(self, item):
        """
        Internal item signal connection.

        @param item  The item to connect to.
        """
        item.dataChanging.connect(self._itemChanging)
        item.dataChanged.connect(self._itemChanged)

    def _itemDisconnect(self, item):
        """
        Internal item signal disconnection.

        @param item  The item to disconnect from.
        """
        item.dataChanging.disconnect()
        item.dataChanged.disconnect()

    def createRoot(self, *args):
        """
        Generates a new instance of the internal data root item given the arguments.

        @param args The list of arguments to pass on the root item.
        """
        return AbstractDataTreeItem(*args)

    def createItem(self, *args):
        """
        Generates a new instance of the internal data item given the arguments.

        @param args The list of arguments to pass on the item.
        """
        return AbstractDataTreeItem(*args)

    def columnCount(self, parent = QtCore.QModelIndex()):
        """
        Returns the number of columns in this model.
        """
        parentItem = self.item(parent)
        return parentItem.columnCount()

    def rowCount(self, parent=QtCore.QModelIndex()):
        """
        Returns the number of rows in this model.
        """
        parentItem = self.item(parent)
        return parentItem.rowCount()

    def data(self, index, role):
        """
        Returns the model data for the corresponding index, filtered by the given role.
        """
        if not index.isValid():
            return None

        item = self.item(index)
        return item.data(index.column(), role) if item else None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Sets the model data at a given index, filtered by the given role to the value.
        """
        item = self.item(index)
        if not item:
            return False

        if not item.setData(index.column(), value, role):
            return False

        return True

    def flags(self, index):
        """
        Get the Qt.ItemFlags for the model data at a given index.

        @param index The lookup key to the data.
        @returns A valid combination of the QtCore.Qt.QFlags enum.
        """
        item = self.item(index)
        if item:
            return item.flags(index.column())
        return QtCore.Qt.NoItemFlags

    def setFlags(self, index, value):
        """
        Sets the Qt.ItemFlags for the model data at a given index.

        @param index The lookup key to the data.
        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        item = self.item(index)
        if item:
            item.setFlags(index.column(), value)

    def insertFlags(self, value):
        """
        Adds the Qt.ItemFlags to the model data for all data.

        @param index The lookup key to the data.
        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        self._flags |= value
        if self._root:
            self._root.insertFlags(value)

    def removeFlags(self, value):
        """
        Removes the Qt.ItemFlags from the model data for all data.

        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        self._flags &= ~value
        if self._root:
            self._root.removeFlags(value)

    def headerData(self, section, orientation, role):
        """
        Returns the Header Data for this model
        """
        if orientation == QtCore.Qt.Horizontal:
            return self._root.data(section, role)

        return None

    def index(self, row, column, parent = QtCore.QModelIndex()):
        """
        Returns the index of the internal data item in the model specified by the given row, column and parent index.

        @param   row The row index into the model
        @param   column The column index into the model
        @param   parent The optional parent QModelIndex
        @returns The QModelIndex of the lookup operation.
        @note    Required for QAbstractItemModel implementation
        """
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        parentItem = self.item(parent)

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def item(self, index):
        """
        Returns the internal data item given the index

        @param index the QModelIndex representing the item
        @returns the respective item if the index is valid; the root item otherwise
        """
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self._root

    def itemIndex(self, item):
        """
        Returns the index for a given item

        @param A item already in the model.
        @returns The QModelIndex of the lookup operation.
        """
        if item == self._root:
            return QtCore.QModelIndex()

        return self.createIndex(item.row(), item.column(), item)

    def parent(self, index):
        """
        Returns the parent index of an index of an internal data item

        @param index The QModelIndex to be used in lookup
        @returns the QModelIndex of the resopetcive parentItem
        @note   Required for QAbstractItemModel implementation
        """
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self._root:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), parentItem.column(), parentItem)

    def appendItem(self, item, parent=QtCore.QModelIndex()):
        """
        Appends an existing AbstractDataTreeItem into the model.

        @param item The item to insert.
        @param parent The index of the parent item in the model.
        @returns The QModelIndex of the insert operation.
        """
        parentItem = self.item(parent)
        nextIndex  = parentItem.childCount()
        lastIndex  = nextIndex

        self.beginInsertRows(parent, nextIndex, lastIndex)

        self._itemInsertPosition(parentItem, item, nextIndex)

        self.endInsertRows()
        return self.itemIndex(item)

    def removeItem(self, item, parent=QtCore.QModelIndex()):
        """
        Removes an existing AbstractDataTreeItem from the model.

        @param item The item to remove.
        @param parent The index of the parent item in the model.
        @returns True if removal was succesful; False otherwise.
        """
        return self.removeRows(item.row(), 1, parent)

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        """
        Removes an existing AbstractDataTreeItem from the model.

        @param item The item to remove.
        @param parent The index of the parent item in the model.
        @returns A list of respective QModelIndexes of the insert operation.
        """
        parentItem = self.item(parent)
        endIndex   = position + rows
        nextIndex  = position
        lastIndex  = endIndex - 1
        items = []
        self.beginInsertRows(parent, nextIndex, lastIndex)

        for i in range(nextIndex, endIndex):
            item = self.createItem()
            items.append(item)
            self._itemInsertPosition(parentItem, item, i)

        self.endInsertRows()
        return [self.itemIndex(item) for item in items]

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):

        parentItem = self.item(parent)
        endIndex   = position + rows
        nextIndex  = position
        lastIndex  = endIndex - 1

        self.beginRemoveRows(parent, nextIndex, lastIndex)

        for i in sorted(range(nextIndex, endIndex), reverse=True):
            self._itemRemovePosition(parentItem, i)

        self.endRemoveRows()
        return True

    def clear(self):
        """
        Clears the model of all data
        """
        if self.hasChildren():
            self.removeRows(0, self.rowCount())

    def reload(self, *args):
        """
        Method to generate the internal data items.

        @param args Optional arguments that affects data generation.
        """
        raise NotImplementedError()

class AbstractDataTableModel(QtCore.QAbstractTableModel):
    """
    The Data Table model provides a Table Item model implementation of a QAbstractTableModel.
    """

    def __init__(self, headerHorData=AbstractData(), headerVerData=AbstractData(), parent=None):
        """
        Constructor

        @param headerHorData The initial horizontal header static data
        @param headerVerData The initial vertical header static data
        @param parent        The QObject parent object.
        """
        super(AbstractDataTableModel, self).__init__(parent)

        self._headerData = {
            QtCore.Qt.Horizontal: headerHorData if isinstance(headerHorData, AbstractData) else AbstractData.BuildData(headerHorData),
            QtCore.Qt.Vertical:   headerVerData if isinstance(headerVerData, AbstractData) else AbstractData.BuildData(headerVerData)
        }
        self._items = []
        self._flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def _dataChanging(self, topLeft, bottomRight=None):
        """
        Internal method to emit the dataChanging signal.

        @param topLeft     The top and left most QtCore.QModelIndex of the data.
        @param bottomRight The bottom and right most QtCore.QModelIndex of the data.
        """
        #self.dataChanging.emit(topLeft, bottomRight or topLeft)

    def _dataChanged(self, topLeft, bottomRight=None):
        """
        Internal method to emit the dataChanged signal.

        @param topLeft     The top and left most QtCore.QModelIndex of the data.
        @param bottomRight The bottom and right most QtCore.QModelIndex of the data.
        """
        self.dataChanged.emit(topLeft, bottomRight or topLeft)

    def _itemInsert(self, item):
        """
        Internal item insert.

        @param item  The item to append to end of the internal collection
        """
        self._items.append(item)
        self._itemConnect(item)

    def _itemInsertPosition(self, item, index):
        """
        Internal item insert.

        @param item  The item to append to end of the internal collection.
        @param index The internal index of the item in the internal collection.
        """
        self._items.insert(index, item)
        self._itemConnect(item)

    def _itemRemove(self, item):
        """
        Internal item removal.

        @param item  The item to remove from the internal collection.
        """
        try:
            self._items.remove(item)
            self._itemDisconnect(item)
        except ValueError:
            pass

    def _itemRemovePosition(self, index):
        """
        Internal item removal.

        @param index  The index of the item to remove from the internal collection.
        """
        try:
            item = self._items.pop(index)
            self._itemDisconnect(item)
        except IndexError:
            pass

    def _itemConnect(self, item):
        """
        Internal item signal connection.

        @param item  The item to connect to.
        """
        item.dataChanging.connect(self._itemChanging)
        item.dataChanged.connect(self._itemChanged)

    def _itemDisconnect(self, item):
        """
        Internal item signal disconnection.

        @param item  The item to disconnect from.
        """
        item.dataChanging.disconnect()
        item.dataChanged.disconnect()

    def _itemChanging(self, id, role):
        """
        Internal item changed event handler.
        """
        item = self.sender()
        index = self.createIndex(item.row(), id, item)
        self._dataChanging(index)

    def _itemChanged(self, id, role):
        """
        Internal item changed event handler.
        """
        item = self.sender()
        index = self.createIndex(item.row(), id, item)
        self._dataChanged(index)

    def createItem(self, *args):
        """
        Generates a new instance of the internal data item given the arguments.

        @param args The list of arguments to pass on the item.
        """
        return AbstractDataItem(*args)

    def columnCount(self, parent = QtCore.QModelIndex()):
        """
        Returns the number of columns in this model.
        """
        return len(self._headerData[QtCore.Qt.Horizontal])

    def rowCount(self, parent = QtCore.QModelIndex()):
        """
        Returns the length of the item list.
        """
        return len(self._items)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        Returns the model data for the corresponding index, filtered by the given role.
        """
        item = self.item(index)
        return item.data(index.column(), role) if item else None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Sets the model data at a given index, filtered by the given role to the value.
        """
        item = self.item(index)
        return item.setData(index.column(), value, role) if item else False

    def flags(self, index):
        """
        Get the Qt.ItemFlags for the model data at a given index.

        @param index The lookup key to the data.
        @returns A valid combination of the QtCore.Qt.QFlags enum.
        """
        item = self.item(index)
        if item:
            return item.flags(index.column())
        return QtCore.Qt.ItemIsEnabled

    def setFlags(self, index, value):
        """
        Sets the Qt.ItemFlags for the model data at a given index.

        @param index The lookup key to the data.
        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        item = self.item(index)
        if item:
            item.setFlags(index.column(), value)

    def insertFlags(self, value):
        """
        Adds the Qt.ItemFlags to the model data for all data.

        @param index The lookup key to the data.
        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        self._flags |= value
        for r in range(self.rowCount()):
            self._items[r].insertFlags(value)

    def removeFlags(self, value):
        """
        Removes the Qt.ItemFlags from the model data for all data.

        @param value A valid combination of the QtCore.Qt.QFlags enum.
        """
        self._flags &= ~value
        for r in range(self.rowCount()):
            self._items[r].removeFlags(value)

    def headerData(self, section, orientation, role):
        """
        Returns the Header Data for this model
        """
        if role != QtCore.Qt.DisplayRole:
            return None

        headerData = self._headerData.get(orientation, None)
        return headerData[role, section] if headerData  else None

    def index(self, row, column, parent = QtCore.QModelIndex()):
        """
        Returns the index of the internal data item in the model specified by the given row, column and parent index.

        @param   row The row index into the model
        @param   column The column index into the model
        @param   parent The optional parent QModelIndex
        @returns The QModelIndex of the lookup operation.
        @note    Required for QAbstractItemModel implementation
        """
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if self._items[row]:
            return self.createIndex(row, column, self._items[row])
        else:
            return QtCore.QModelIndex()

    def item(self, index):
        """
        Returns the internal data item given the index

        @param index the QModelIndex representing the item
        @returns the respective item if the index is valid; the root item otherwise
        """
        if isinstance( index, int ):
            return self._items[index]

        if isinstance( index, ( QtCore.QModelIndex ) ) and index.isValid():
            item = index.internalPointer()
            if item:
                return item
            return self._items[index.row()]

        return None

    def itemIndex(self, item):
        """
        Returns the index for a given item

        @param A item already in the model.
        @returns The QModelIndex of the lookup operation.
        """
        for r in range(len(self._items)):
            if self._items[r] == item:
                return self.createIndex(r, 0, self._items[r])
            c = self._items[r].dataIndex(item)
            if c != -1:
                return self.createIndex(r, c, self._items[r])

        return QtCore.QModelIndex()

    def appendItem(self, item):
        """
        Appends an existing AbstractDataItem into the model.

        @returns The QModelIndex of the insert operation.
        """
        self.beginInsertRows(QtCore.QModelIndex(), len(self._items), len(self._items))

        self._itemInsert(item)

        self.endInsertRows()
        return self.itemIndex(item)

    def removeItem(self, item):
        """
        Remove an existing AbstractDataItem from the model.

        @returns True if the remove operation was succesful; False otherwise.
        """
        return self.removeRows(self.index(item).row())

    def removeIndex(self, index):
        """
        Remove an existing AbstractDataItem from the model.
        """
        return self.removeRows(index.row())

    def insertRows(self, position, rows=1, index=QtCore.QModelIndex()):
        """
        Insert a rows with an empty DataItems into the model.
        """
        endIndex  = position + rows
        nextIndex = position
        lastIndex = endIndex - 1
        items = []
        self.beginInsertRows(QtCore.QModelIndex(), nextIndex, lastIndex)

        for i in range(nextIndex, endIndex):
            item = self.createItem()
            items.append(item)
            self._itemInsertPosition(item, i)

        self.endInsertRows()
        return [self.itemIndex(item) for item in items]

    def removeRows(self, position, rows=1, index=QtCore.QModelIndex()):
        """
        Remove a row from the model.
        """
        endIndex  = position + rows
        nextIndex = position
        lastIndex = endIndex - 1
        self.beginRemoveRows(QtCore.QModelIndex(), nextIndex, lastIndex)

        # Reverse sort to iterate and delete at the same
        for i in sorted(range(nextIndex, endIndex), reverse=True):
            self._itemRemovePosition(i)

        self.endRemoveRows()
        return True

    def clear(self):
        """
        Clears the model of all data
        """
        self.removeRows(0, self.rowCount())

    def reload(self, *args):
        """
        Method to generate the internal data items.

        @param args Optional arguments that affects data generation.
        """
        raise NotImplementedError()

class AbstractDataChangeValueCommand(QtGui.QUndoCommand):

    def __init__(self, index, value, model, text=None, parent=None):
        super(ChangeValueCommand, self).__init__(text, parent)

        self._model = model

        self._row = index.row()
        self._col = index.column()
        self._oldvalue = index.data(QtCore.Qt.DisplayRole)
        self._newvalue = value

        if not text:
            self.setText("({0},{1}) => [{2}] to [{3}]".format(self._row, self._col, self._oldvalue, self._newvalue))

    def redo(self):
        super(ChangeValueCommand, self).redo()
        index = self._model.index(self._row, self._col)
        item  = self._model.item(index)
        item.setData(self._col, self._newvalue, QtCore.Qt.EditRole)

    def undo(self):
        super(ChangeValueCommand, self).undo()
        index = self._model.index(self._row, self._col)
        item  = self._model.item(index)
        item.setData(self._col, self._oldvalue, QtCore.Qt.EditRole)
