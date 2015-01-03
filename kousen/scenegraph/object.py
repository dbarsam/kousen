# -*- coding: utf-8 -*-
"""
This module provides object specializations of transformation nodes.
"""
from PySide import QtCore, QtGui
from kousen.scenegraph.transform import TransformationNode

class ObjectNode(TransformationNode):
    """
    The ObjectNode extends the TransformationNode with the functionality to represent a physical entity in the Scene Graph.
    """
    # Additional Meta Information
    __category__       = "Object Node"
    __icon__           = ":/icons/node.png"
    __description__    = "<Unknown Primitive>"
    __selectioncolor__ = QtGui.QColor(255, 0, 0)

    nodeSelected = QtCore.Signal(bool)

    def __init__(self, name, parent):
        """
        Constructor.

        @param name    The display name of the node.
        @param parent  The initial AbstractDataTreeItem-derived parent.
        """
        super(ObjectNode, self).__init__(name, parent)

        # Initial color of the object.
        self.__color = QtGui.QColor(0, 255, 0)
        self.__selected = False

    @property
    def selected(self):
        """
        Convenience property to access the selection state of the object node.

        @returns True if the object is selected; False otherwise.
        """
        return self.__selected

    @selected.setter
    def selected(self, value):
        """
        Convenience property to access the selection state of the object node.

        @param value True if the object is to be selected; False otherwise.
        """
        self.__selected = value

    @property
    def color(self):
        """
        Convenience property to access the color state of the object node.

        @returns A QtGui.QColor instance.
        """
        if self.__selected:
            return self.__primitive_selectioncolor__
        return self.__color

    @color.setter
    def color(self, value):
        """
        Convenience property to access the color state of the object node.

        @param value A QtGui.QColor instance.
        """
        self.__color = value

    def setColor(self, color):
        """
        Sets the color property for this node and all children nodes

        @param value A QtGui.QColor instance.
        """
        self.color = color
        for child in self.children():
            child.setColor(color)
