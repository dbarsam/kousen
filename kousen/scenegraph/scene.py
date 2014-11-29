# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
from kousen.core.abstractmodel import AbstractData, AbstractDataFields, AbstractDataItem, AbstractDataTreeItem, AbstractDataListModel, AbstractDataTreeModel

class AbstractSceneItemData(AbstractData):
    """
    The AbstractSceneItemData represents a simplied AbstractData configured specifically for a AbstractSceneGraphItem.
    """
    def __init__(self, name, icon, description, parent=None):
        """
        Constructor.

        @param name         The name value.
        @param icon         The decoration value.
        @param description  The tool tip decoration value.
        @param parent       The initial parent AbstractDataTreeItem.
        """
        super(AbstractSceneItemData, self).__init__(None, parent)
        self[QtCore.Qt.DisplayRole, AbstractSceneGraphItem.Fields.NAME]        = name
        self[QtCore.Qt.DecorationRole, AbstractSceneGraphItem.Fields.NAME]     = QtGui.QIcon(QtGui.QPixmap(icon))
        self[QtCore.Qt.ToolTipRole, AbstractSceneGraphItem.Fields.NAME]        = description
        self[QtCore.Qt.AccessibleTextRole, AbstractSceneGraphItem.Fields.NAME] = name
        self[QtCore.Qt.EditRole, AbstractSceneGraphItem.Fields.NAME]           = name

class AbstractSceneGraphItem(AbstractDataTreeItem):
    """
    The AbstractSceneGraphItem represents an entry an the AbstractSceneGraphModel.
    """

    class Fields(AbstractDataFields):
        """
        The Fields class provides an enumeration of the various fields within a AbstractSceneGraphItem.
        """
        NAME = 0

    @classmethod
    def subclasses(cls, recursive = True):
        """
        Calculates all derived subclasses.

        @param   recursive True if the subclass search should recusively delve into the inheritance tree.
        @returns           A list of SceneraphItem-derived class type.
        """
        sb = cls.__subclasses__()
        if recursive:
            for c in cls.__subclasses__():
                sb.extend(c.subclasses())
        return sb

    @classmethod
    def instantiable(cls):
        """
        Calculates if this Scene Graph Item derived class is instatiable (i.e. it can be created by the user)

        @returns True if the item can be directly instantiated; False otherwise.
        """
        return False

    def __init__(self, sdata, parent):
        """
        Constructor.

        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial AbstractDataTreeItem-derived parent of this AbstractSceneGraphItem
        """
        super(AbstractSceneGraphItem, self).__init__(sdata, parent)
        self._restore = {}

    def reset(self):
        """
        Resets the non-constant components of the class.
        """
        for key in self._restore:
            self.__dict__[key] = self._restore[key]

    def size(self):
        """
        Calculates the data item size (i.e. columns) of this item.

        @returns The size of the field list.
        """
        return self.Fields.size()

    def filter(self, condition):
        """
        Generates an inclusive list of node and children based on a boolean expression evaluation.

        @param   condition A lambda expression used to recursively evaluate each node.
        @returns           A list of AbstractSceneGraphItem that succesfully evaluate the condition.
        """
        result = [self] if condition(self) else []
        for child in self._children:
            result += child.filter(condition)
        return result

class SceneGraphNode(AbstractSceneGraphItem):
    """
    The Scene Graph Node represents a common node in a scene graph hierarchy.
    """
    # Additional Meta Information
    __category__     = "<unknown>"
    __description__  = "<Invalid Scene Graph Item>"
    __icon__         = None
    __instantiable__ = False

    def __init__(self, name, parent):
        """
        Constructor.

        @param name    The initial name of the node.
        @param parent  The initial AbstractSceneGraphItem-derived parent of this AbstractSceneGraphItem.
        """
        super(SceneGraphNode, self).__init__(AbstractSceneItemData(name, self.__icon__, self.__description__), parent)

class SceneGraphRoot(AbstractSceneGraphItem):
    """
    The Scene Graph Root represents a top-most node in a scene graph hierarchy.
    """
    # Additional Meta Information
    __category__     = "<unknown>"
    __description__  = "<Invalid Scene Graph Item>"
    __icon__         = None
    __instantiable__ = False

    def __init__(self, sdata):
        """
        Constructor.

        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        """
        super(SceneGraphRoot, self).__init__(sdata, None)
        self._internal = sdata

class AbstractSceneGraphModel(AbstractDataTreeModel):
    """
    The Scene Model represents a complete scene hierarchy.
    """
    SceneGraphItemType = []

    def __init__(self, parent):
        """
        Constructor.

        @param headerdata The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent     The initial parent AbstractDataTreeItem of this AbstractDataTreeItem
        """
        super(AbstractSceneGraphModel, self).__init__(AbstractSceneGraphItem.Fields.headerdata(), parent)
        self._camera = None

    @property
    def activeCamera(self):
        """
        Convenience property to access the Scene Graph Model's active Camera Node

        @returns A Camera Node if valid; None otherwise.
        """
        return self._camera

    @activeCamera.setter
    def activeCamera(self, value):
        """
        Convenience property to access the Scene Graph Model's active Camera Node

        @param value An instance of a Camera Node.
        """
        self._camera = value

    def createRoot(self, *args):
        """
        Implements the AbstractDataTreeModel's createRoot method.

        @param   args A variable size list of arguments to be passed to the created root node.
        @returns  An instantiated root node.
        """
        return SceneGraphRoot(*args)

    def createItem(self, *args):
        """
        Implements the AbstractDataTreeModel's createItem method.

        @param   args A variable size list of arguments to be passed to the created node.
        @returns  An instantiated node.
        """
        return SceneGraphNode(*args)

    def filter(self, condition):
        """
        Generates an inclusive list of node and children based on a boolean expression evaluation.

        @param   condition A lambda expression used to recursively evaluate each node.
        @returns           A list of AbstractSceneGraphItem that succesfully evaluate the condition.
        """
        return self._root.filter(condition)

class SceneGraphType(AbstractDataTreeItem):
    """
    The Scene Item Type Item represents a type of a component of the scene in the scene hierarchy.
    """
    class Fields(AbstractDataFields):
        """
        The Fields class provides an enumeration of the various fields within a AbstractSceneGraphItem.
        """
        NAME  = 0
        CLASS = 1

    def __init__(self, sdata={}, parent=None):
        """
        Constructor.

        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial parent AbstractDataTreeItem of this AbstractDataTreeItem
        """
        super(SceneGraphType, self).__init__(sdata, parent)

    def size(self):
        """
        Calculates the data item size (i.e. columns) of this item.

        @returns The size of the field list.
        """
        return self.Fields.size()

class SceneGraphTypeTreeModel(AbstractDataTreeModel):
    """
    The Scene Model represents a complete scene hierarchy.
    """

    def __init__(self, headerdata, parent=None):
        """
        Constructor.

        @param headerdata The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent     The initial parent AbstractDataTreeItem of this AbstractDataTreeItem
        """
        super(SceneGraphTypeTreeModel, self).__init__(headerdata, parent)

    def createRoot(self, *args):
        """
        Implements the AbstractDataTreeModel's createRoot method.

        @param   args A variable size list of arguments to be passed to the created root node.
        @returns  An instantiated root node.
        """
        return SceneGraphType(*args)

    def createItem(self, *args):
        """
        Implements the AbstractDataTreeModel's createItem method.

        @param   args A variable size list of arguments to be passed to the created node.
        @returns  An instantiated node.
        """
        return SceneGraphType(*args)

    def reload(self, *args):
        """
        Implements the AbstractDataTreeModel's reload method.

        @param   args A variable size list of arguments to be evaluated during reloading.
        """
        from itertools import groupby

        self.beginResetModel()
        self.clear()

        classes = sorted([c for c in AbstractSceneGraphItem.subclasses() if c.__instantiable__], key=(lambda x: x.__category__))
        for key, group in groupby(classes, lambda x: x.__category__):
            subroot = self.createItem([key, None], None)
            qindex = self.appendItem(subroot)
            parentIndex = self.itemIndex(subroot)
            for groupitem in group:
                sdata = AbstractData.BuildData([groupitem.__description__, groupitem])
                if groupitem.__icon__:
                    sdata[QtCore.Qt.DecorationRole, AbstractSceneGraphItem.Fields.NAME] = QtGui.QIcon(QtGui.QPixmap(groupitem.__icon__))
                subitem = self.createItem(sdata, None)
                self.appendItem(subitem, parentIndex)

        self.endResetModel()


