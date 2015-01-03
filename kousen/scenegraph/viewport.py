# -*- coding: utf-8 -*-
"""
This module provides viewport specializations of scene graph nodes.

A Viewport defines a abstract rectangle, often taking the role of a virtual camera.
"""
import abc
from kousen.scenegraph import SceneGraphNode

class VirtualScreen(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def resize(self, width, height):
        """
        Resizes the virtual screen.

        @param width  The width (in pixels) of the virtual screen.
        @param height The height (in pixels) of the virtual screen.
        """
        raise NotImplementedError("resize has not been implemented.")

class ViewportNode(SceneGraphNode, VirtualScreen):
    """
    ViewportNode provides a Viewport implementation of a SceneGraphNode.
    """
    # Additional Meta Information
    __category__     = "HUD Node"
    __icon__         = ":/icons/hud.png"
    __instantiable__ = False

    # Screen default values
    __screen_left__     = 0
    __screen_right__    = 1
    __screen_top__      = 0
    __screen_bottom__   = 1
    __screen_znear__    = 0
    __screen_zfar__     = 1

    def __init__(self, name, parent):
        """
        Constructor.

        @param name    The display name of the node.
        @param parent  The initial AbstractDataTreeItem-derived parent.
        """
        super(ViewportNode, self).__init__(name, parent)
        self._left   = self.__screen_left__
        self._right  = self.__screen_right__
        self._top    = self.__screen_top__
        self._bottom = self.__screen_bottom__
        self._znear  = self.__screen_znear__
        self._zfar   = self.__screen_zfar__

    def resize(self, width, height):
        """
        Resizes the virtual screen.

        @param width  The width (in pixels) of the virtual screen.
        @param height The height (in pixels) of the virtual screen.
        """
        self._left   = 0
        self._right  = width
        self._top    = 0
        self._bottom = height