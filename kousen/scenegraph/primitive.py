# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
from kousen.scenegraph.scene import SceneGraphItem

class PrimitiveNode(SceneGraphItem):
    """
    Base class for any object designated as a geometric primitive.
    """
    # Additional Meta Information
    __category__     = "Primitive Node"
    __icon__         = ":/icons/node.png"
    __description__  = "<Unknown Primitive>"

    def __init__(self, name, parent):
        """
        Constructor.

        @param name    The display name of the node.
        @param parent  The initial parent AbstractDataTreeItem of this AbstractDataTreeItem
        """
        super(PrimitiveNode, self).__init__({}, parent) 
        
        self._staticdata[QtCore.Qt.DisplayRole, SceneGraphItem.Fields.NAME]        = name or self.__label__
        self._staticdata[QtCore.Qt.DecorationRole, SceneGraphItem.Fields.NAME]     = QtGui.QIcon(QtGui.QPixmap(self.__icon__))
        self._staticdata[QtCore.Qt.ToolTipRole, SceneGraphItem.Fields.NAME]        = name or self.__description__
        self._staticdata[QtCore.Qt.AccessibleTextRole, SceneGraphItem.Fields.NAME] = name or self.__description__
        self._staticdata[QtCore.Qt.EditRole, SceneGraphItem.Fields.NAME]           = name or self.__description__
