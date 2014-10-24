from PySide import QtGui, QtCore

from kousen.core.abstractmodel import AbstractData, AbstractDataFields, AbstractDataItem, AbstractDataTreeItem, AbstractDataListModel, AbstractDataTreeModel

class PropertyItem(AbstractDataTreeItem):
    """
    The Property Item represents a single Python property objects of an object.
    """    

    class Fields(AbstractDataFields):
        """
        The Fields class provides an enumeration of the various fields within a PropertyItem.
        """
        NAME  = 0
        VALUE = 1

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

    def size(self):
        """
        Calculates the data item size (i.e. columns) of this item.

        @returns The size of the field list.
        """
        return self.Fields.size()

    def data(self, id, role=QtCore.Qt.DisplayRole):
        """
        Gets the data for the corresponding id, filtered by the given role.

        @param id   The lookup key to the data.
        @param role The filter key of the lookup operation.
        @returns    The data if the lookup operation was succesful; False otherwise.
        """
        if id == self.Fields.VALUE:
            if role == QtCore.Qt.DisplayRole:
                return str(self.fget());

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

        return super(PropertyItem, self).data(id, role)

class PropertyRoot(AbstractDataTreeItem):
    """
    The Property Root represents an invisible root item in the Property Model.
    """    

    class Fields(AbstractDataFields):
        """
        The Fields class provides an enumeration of the various fields within a PropertyRoot.
        """
        NAME  = 0
        VALUE = 1

    def __init__(self, sdata=[], parent=None):
        """
        Constructor.

        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial parent AbstractDataTreeItem of this PropertyItem
        """        
        super(PropertyRoot, self).__init__(sdata, parent)

    def size(self):
        """
        Calculates the data item size (i.e. columns) of this item.

        @returns The size of the field list.
        """
        return self.Fields.size()

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

        # We key property items by a (class type, property name) dictionary
        self._propertyTable = {}

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

    def insertProperties(self, objects):
        """
        Inserts a list of Python property objects derived from a list of objects.

        @param objects A list of objects to examine for Python property objects.
        """
        import inspect

        for object in objects:
            # Property obects exist at the class defintion; get the members of the object 
            # and match them up with the class defition.
            for name, value, pobject in [(n, v, getattr(object.__class__, n, None)) for (n, v) in inspect.getmembers(object)]:
                if not (pobject and isinstance(pobject, property)):
                    continue

                # Create (or get) the class-propertyname lookup table entry and add the
                # object to the proprty item's object list (to handle multiple instance
                # of the same class).
                classdict = self._propertyTable.setdefault(object.__class__, {})
                pitem = classdict.get(name, None)
                if not pitem:
                    pitem = self.createItem(name, pobject, self._root)
                    self._propertyTable[object.__class__][name] = pitem
                    self.appendItem(pitem)
                pitem.insertComponent(object)

    def removeProperties(self, objects):
        """
        Removes all respective Python property objects derived from an list of objects.

        @param objects A list of objects to examine for Python property objects.
        """
        for object in objects:
            # Get the entire class lookup table entry for the class and remove the object
            # and if it is the last object in multiple selection remove the model data.
            classdict = self._propertyTable.get(object.__class__, {})
            for name, pitem in [(k, classdict[k]) for k in list(classdict.keys())]:                
                pitem.removeComponent(object)                    
                if pitem.isEmpty():
                    self.removeItem(pitem)
                    del classdict[name]
