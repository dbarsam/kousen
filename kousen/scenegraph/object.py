# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
from kousen.scenegraph.transform import TransformationNode

class ObjectNode(TransformationNode):
    """
    The ObjectNode extends the TransformationNode with the functionality to represent a physical entity in the Scene Graph.
    """
    # Additional Meta Information
    __category__     = "Object Node"
    __icon__         = ":/icons/node.png"
    __description__  = "<Unknown Primitive>"

    def __init__(self, name, parent):
        """
        Constructor.

        @param name    The display name of the node.
        @param parent  The initial AbstractDataTreeItem-derived parent.
        """
        super(ObjectNode, self).__init__(name, parent)