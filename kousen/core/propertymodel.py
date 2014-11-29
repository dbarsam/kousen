# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore

from kousen.core.abstractmodel import AbstractData, AbstractDataFields, AbstractDataItem, AbstractDataTreeItem, AbstractDataListModel, AbstractDataTreeModel

class AbstractPropertyItem(AbstractDataTreeItem):
    """
    The Abstract Property Item represents a base layer of functionality in the Property Model.
    """

    class Fields(AbstractDataFields):
        """
        The Fields class provides an enumeration of the various fields within a PropertyItem.
        """
        NAME  = 0
        VALUE = 1

    def __init__(self, sdata, parent=None):
        """
        Constructor.

        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial parent AbstractDataTreeItem of this AbstractPropertyItem
        """
        super(AbstractPropertyItem, self).__init__(sdata, parent)
        
        # We key property items by a (class type, property name) dictionary
        self._childrenPropertyTable = {}

    def size(self):
        """
        Calculates the data item size (i.e. columns) of this item.

        @returns The size of the field list.
        """
        return self.Fields.size()

    def getPropertyItem(self, class_name, property_name):
        """
        Returns the PropertyItem associated with the class name, property name pair

        @param class_name    The primary key used to store property items.
        @param property_name The secondary key used to store property items.
        @returns             The PropertyItem is available; None otherwise.
        """
        classdict = self._childrenPropertyTable.get(class_name, {})
        return classdict.get(property_name, None)

    def getPropertyItems(self, class_name):
        """
        Returns all PropertyItems associated with the class name.

        @param class_name    The primary key used to store property items.
        @returns             A list of applicable PropertyItems
        """
        subdict = self._childrenPropertyTable.get(class_name, {})
        return [(k, subdict[k]) for k in subdict.keys()]

    def insertPropertyItem(self, class_name, property_name, item):
        """
        Inserts a PropertyItem and associates it with a class name, property name pair.

        @param class_name    The primary key used to store property items.
        @param property_name The secondary key used to store property items.
        @param item          The PropertyItem instance.
        @returns             The PropertyItem is available; None otherwise.
        """
        subdict = self._childrenPropertyTable.setdefault(class_name, {})
        subdict[property_name] = item

    def removePropertyItem(self, class_name, property_name):
        """
        Removes a PropertyItem associated with a class name, property name pair.

        @param class_name    The primary key used to store property items.
        @param property_name The secondary key used to store property items.
        """
        subdict = self._childrenPropertyTable.get(class_name, None)
        if subdict:
            subdict.pop(property_name, None)
            if not subdict:
                self._childrenPropertyTable.pop(class_name, None)

class PropertyItem(AbstractPropertyItem):
    """
    The Property Item represents a single Python property objects of an object.
    """

    # Define a table of roles and respective types that return the property value
    roleValues = { QtCore.Qt.DecorationRole : [QtGui.QColor] }

    def __init__(self, name=None, property=None, parent=None):
        """
        Constructor.

        @param name       The name of the property item.
        @param property   The property object assigned to the name.
        @param parent     The initial parent AbstractDataTreeItem of this PropertyItem
        """
        super(PropertyItem, self).__init__(AbstractData.BuildData([name]), parent)

        # The property
        self._property = property
        if self._property.fset:
            self._staticdata[AbstractData.FlagRole, PropertyItem.Fields.VALUE] = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

        # The list of component with the property for which to retrieve the value.
        self._components = set()

    def fget(self):
        """
        Invokes the property object's fget method.

        @return A single value that is consistent across all components; None if not applicable.
        """
        values = [self._property.fget(c) for c in self._components]
        return values[0] if values and all(v == values[0] for v in values) else None

    def fset(self, value):
        """
        Invokes the property object's fset method.

        @param value  The value to use in the property's fset method.
        """
        for c in self._components:
            self._property.fset(c, value)

    def insertComponent(self, component):
        """
        Inserts an object into this item's Python property object component list.

        @param component An object with the property for which to retrieve the value.
        """
        self._components.add(component)

    def removeComponent(self, component):
        """
        Removes an object from this item's property object component list.

        @param component An object with the property for which to retrieve the value.
        """
        self._components.discard(component)

    def isEmpty(self):
        """
        Calculates if the component list is empty.

        @returns True if there are no components; False otherwise.
        """
        return not bool(self._components)

    def data(self, id, role=QtCore.Qt.DisplayRole):
        """
        Gets the data for the corresponding id, filtered by the given role.

        @param id   The lookup key to the data.
        @param role The filter key of the lookup operation.
        @returns    The data if the lookup operation was succesful; False otherwise.
        """
        if id == self.Fields.VALUE:
            if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
                return self.fget()
            if role in self.roleValues:
                value = self.fget()
                if type(value) in self.roleValues[role]:
                    return self.fget()

        return super(PropertyItem, self).data(id, role)

    def setData(self, id, value, role=QtCore.Qt.EditRole):
        """
        Sets the data for the corresponding id, filtered by the given role.

        @param id   The lookup key to the data.
        @param role The filter key of the data storing operation.
        @returns    True is operation was succesful; False otherwise.
        """
        if id == self.Fields.VALUE and role == QtCore.Qt.EditRole:
            self.dataChanging.emit(id, role)
            self.fset(value)
            self.dataChanged.emit(id, role)
            return True

        return super(PropertyItem, self).setData(id, role)

class PropertyRoot(AbstractPropertyItem):
    """
    The Property Root represents an invisible root item in the Property Model.
    """

    def __init__(self, sdata=[], parent=None):
        """
        Constructor.

        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial parent AbstractDataTreeItem of this PropertyItem
        """
        super(PropertyRoot, self).__init__(sdata, parent)

class PropertyModel(AbstractDataTreeModel):
    """
    The Property Model represents a complete list of Python property objects.
    """
    def __init__(self, headerdata, parent=None):
        """
        Constructor.

        @param headerdata The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent     The initial parent PropertyModel of this AbstractDataTreeItem
        """
        super(PropertyModel, self).__init__(headerdata, parent)

    def createRoot(self, *args):
        """
        Implements the AbstractDataTreeModel's createRoot method.

        @param   args A variable size list of arguments to be passed to the created root node.
        @returns  An instantiated root node.
        """
        return PropertyRoot(*args)

    def createItem(self, *args):
        """
        Implements the AbstractDataTreeModel's createItem method.

        @param   args A variable size list of arguments to be passed to the created node.
        @returns  An instantiated node.
        """
        return PropertyItem(*args)

    def insertProperties(self, objects, parent=QtCore.QModelIndex()):
        """
        Inserts a list of Python property objects derived from a list of objects.

        @param objects A list of objects to examine for Python property objects.
        """
        import inspect
        parentItem = self.item(parent)
        for object in objects:
            # Property obects exist at the class defintion; get the members of the object
            # and match them up with the class defition.
            for name, value, pobject in [(n, v, getattr(object.__class__, n, None)) for (n, v) in inspect.getmembers(object)]:
                if not (pobject and isinstance(pobject, property)):
                    continue

                # Create (or get) the class-propertyname lookup table entry and add the
                # object to the proprty item's object list (to handle multiple instance
                # of the same class).
                pitem = parentItem.getPropertyItem(object.__class__, name)
                if not pitem:
                    pitem = self.createItem(name, pobject, parentItem)
                    self.appendItem(pitem, parent)
                    parentItem.insertPropertyItem(object.__class__, name, pitem)
                pitem.insertComponent(object)
                
                # Insert any child properties
                self.insertProperties([pobject.fget(object)], self.itemIndex(pitem))

    def removeProperties(self, objects, parent=QtCore.QModelIndex()):
        """
        Removes all respective Python property objects derived from an list of objects.

        @param objects A list of objects to examine for Python property objects.
        """
        parentItem = self.item(parent)

        for object in objects:
            # Get the entire class lookup table entry for the class and remove the object
            # and if it is the last object in multiple selection remove the model data.
            items = list(parentItem.getPropertyItems(object.__class__))
            for name, pitem in items:
                pitem.removeComponent(object)
                if pitem.isEmpty():
                    self.removeItem(pitem, parent)
                    parentItem.removePropertyItem(object.__class__, name)