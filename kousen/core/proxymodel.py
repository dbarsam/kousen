from PySide import QtGui, QtCore

class ColumnFilterProxyModel(QtGui.QSortFilterProxyModel):
    """
    Sub Class of QSortFilterProxyModel to show|hide rows based their column values
    """
    def __init__(self, parent=None):
        super(ColumnFilterProxyModel, self).__init__(parent)
        self.__columnFilter = {}

    def setColumnFilter(self, column, filterCondition):
        """
        Sets a lambda to be evaluted with the value of the row at the column index
        @param column: The column index used in the QtCore.QModelIndex requires by the model's data method
        @param filterCondition: A lambda expression x => bool where x is the model's value and row, column
        """
        self.__columnFilter[column] = filterCondition
        self.invalidateFilter()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        """
        Overridden method to returns true if the item in the row indicated by the given source_row and source_parent should be included in the model; otherwise returns false.
        """
        #Get the fileinfo of the item
        model = self.sourceModel()
        
        # Extract the Column and the Column's value and apply the filter function.
        # We currently filter on the raw data (UserRole) not the DisplayData
        for columnIndex in self.__columnFilter:
            filter = self.__columnFilter[columnIndex]
            value = model.data(model.createIndex(sourceRow, columnIndex), self.filterRole())
            if not filter(value):
                return False

        return super(ColumnFilterProxyModel, self).filterAcceptsRow(sourceRow, sourceParent)


class ColumnFilterDataProxyModel(QtGui.QSortFilterProxyModel):
    """
    Sub Class of QSortFilterProxyModel to override data based on their column values
    """
    def __init__(self, parent=None):
        super(ColumnFilterDataProxyModel, self).__init__(parent)
        self.__filterData = {}
        self.__filteredIndexes = []

    def filterAcceptsRow(self, sourceRow, sourceParent):
        """
        Overridden method to returns true if the item in the row indicated by the given source_row and source_parent should be included in the model; otherwise returns false.
        """
        return True

    def setFilterData(self, role, data):
        """
        Sets a data override to return if the data passes the filter.

        @param role The data role.
        @param data The override data
        """
        self.__filterData[role] = data

    def filterAcceptsIndex(self, index):
        """
        Applies QSortFilterProxyModel filtering algorithm on an index cell instead of a row.
        """        
        if self.filterRegExp().isEmpty():
            return True
        
        if self.filterKeyColumn() >= 0 and index.column() != self.filterKeyColumn():
            return True

        data = super(ColumnFilterDataProxyModel, self).data(index, self.filterRole())
        if not data:
            return False
        
        return self.filterRegExp().indexIn(str(data)) >= 0

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        Returns the model data for the corresponding index, filtered by the given role.
        """
        if not self.filterRegExp().isEmpty():
            override = self.__filterData.get(role, None)
            if override and self.filterAcceptsIndex(index):
                return override

        return super(ColumnFilterDataProxyModel, self).data(index, role)

class TreeColumnFilterProxyModel(ColumnFilterProxyModel):
    """
    Sub Class of ColumnFilterProxyModel to show|hide rows in a TreeView
    """
    def __init__(self, parent=None):
        """
        Constructor.

        @param sourceModel The initial source model.
        """
        super(TreeColumnFilterProxyModel, self).__init__(parent)
 
    def filterAcceptsRow(self, sourceRow, sourceParent):
        """
        Overridden method to returns true if the item in the row indicated by the given source_row and source_parent should be included in the model; otherwise returns false.
        """
        # Test the row via the base class.
        if super(TreeColumnFilterProxyModel, self).filterAcceptsRow(sourceRow, sourceParent): 
            return True

        model = self.sourceModel()
        index = model.index(sourceRow, 0, sourceParent)
        
        # Test Root - Root Is Always Valid
        if not index.isValid():
            return True
        
        # Test the Children
        return any(self.filterAcceptsRow(i, index) for i in range(index.model().rowCount(index)))

class UndoRedoProxyModel(QtGui.QSortFilterProxyModel):
    """
    Sub Class of QSortFilterProxyModel to provide undo|redo functionality
    See http://doc.qt.digia.com/qq/qq25-undo.html for more information
    """
    def __init__(self, sourceModel = None, parent = None):
        """
        Constructor.

        @param sourceModel The initial source model.
        """
        super(UndoRedoProxyModel, self).__init__(parent)
        self.setSourceModel(sourceModel)
        self._undostack = QtGui.QUndoStack(self)

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
        if not index.isValid():
            return false
        if value == index.data(role):
            return false
        
        command = ProxySetDataCommand(index, value, role, self)
        self._undostack(command)
        
        item = self.item(index)
        return item.setData(index.column(), value, role) if item else False
