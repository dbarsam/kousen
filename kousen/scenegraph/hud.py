# -*- coding: utf-8 -*-
import math
from PySide import QtGui, QtCore
from OpenGL import GL
from OpenGL import GLU
from OpenGL import GLUT
from kousen.scenegraph import SceneGraphItem
from kousen.math import Point3D, Vector3D, Matrix4x4
from kousen.gl.glutil import GLUQuadricScope, GLScope, GLVariableScope, GLAttribScope, GLClientAttribScope, GLMatrixScope

class CameraHUDNode(SceneGraphItem):
    """
    The Camera HUD Node provides a Camera Data HUD implementation of a SceneGraphItem.
    """
    # Additional Meta Information
    __category__     = "HUD Node"
    __icon__         = ":/icons/hud-camera.png"

    # HUD default values
    __screen_left__     = 0
    __screen_right__    = 1
    __screen_top__      = 0
    __screen_bottom__   = 1
    __screen_znear__    = 0
    __screen_zfar__     = 1

    def __init__(self, camera, parent):
        """
        Constructor.

        @param camera   An instance of CameraNode to monitor.
        @param parent   The parent SceneGraphItem instance.
        """
        super(CameraHUDNode, self).__init__({}, parent) 
        self._left   = self.__screen_left__
        self._right  = self.__screen_right__
        self._top    = self.__screen_top__
        self._bottom = self.__screen_bottom__
        self._znear  = self.__screen_znear__
        self._zfar   = self.__screen_zfar__

        self._transform = Matrix4x4()

        self._camera = camera

        self._staticdata[QtCore.Qt.DisplayRole, SceneGraphItem.Fields.NAME]        = "CameraHUD"
        self._staticdata[QtCore.Qt.DecorationRole, SceneGraphItem.Fields.NAME]     = QtGui.QIcon(QtGui.QPixmap(self.__icon__))  
        self._staticdata[QtCore.Qt.ToolTipRole, SceneGraphItem.Fields.NAME]        = "CameraHUD"
        self._staticdata[QtCore.Qt.AccessibleTextRole, SceneGraphItem.Fields.NAME] = "CameraHUD"
        self._staticdata[QtCore.Qt.EditRole, SceneGraphItem.Fields.NAME]           = "CameraHUD"

    @property
    def camera(self):
        """
        Convenience property to access the monitored Camera Node.

        @returns An instance of a CameraNode if valid; None otherwise.
        """ 
        return self._camera
    
    @camera.setter
    def camera(self, value):
        """
        Convenience property to access the monitored Camera Node.

        @param value An instance of a CameraNode.
        """ 
        self._camera = value

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

