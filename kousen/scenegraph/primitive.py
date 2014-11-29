# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
from kousen.scenegraph.object import ObjectNode

class PrimitiveNode(ObjectNode):
    """
    PrimitiveNode provides a base class for all gemetric object implementation of an ObjectNode.
    """
    # Additional Meta Information
    __category__     = "Primitive Node"
    __icon__         = ":/icons/node.png"
    __description__  = "<Unknown Primitive>"

    def __init__(self, name, parent):
        """
        Constructor.

        @param name    The display name of the node.
        @param parent  The initial AbstractDataTreeItem-derived parent.
        """
        super(PrimitiveNode, self).__init__(name, parent)