# -*- coding: utf-8 -*-
import math
from PySide import QtGui, QtCore
from OpenGL import GL
from kousen.gl.glscene import GLNode
from kousen.scenegraph import CameraNode
from kousen.math import Matrix4x4
from kousen.math.conic import coniclength, conicwidth

class GLCameraNode(GLNode, CameraNode):
    """
    The GL Camera Node provides an OpenGL implementation of a CameraNode.
    """
    # Additional Meta Information
    __category__     = "OpenGL Camera Node"
    __description__  = "Perspective Camera Node"
    __instantiable__ = True

    def __init__(self, position=None, target=None, up=None, fov=None, znear=None, zfar=None, swidth=None, sheight=None, parent=None):
        """
        Constructor.

        @param position The position of the camera (in world space). If None, it will default to CameraNode.__camera_target__.
        @param target   The camera target point (in world space).  If None, it will default to CameraNode.__camera_position__.
        @param up       The camera up point (in world space). If None, it will default to CameraNode.__camera_upvector__.
        @param fov      The field of view (in degrees). If None, it will default to CameraNode.__camera_fov__.
        @param znear    The distance from position to the near clipping plane. If None, it will default to CameraNode.__camera_znear__.
        @param zfar     The distance from position to the far clipping plane. If None, it will default to CameraNode.__camera_zfar__.
        @param swidth   The initial screen width (in pixels). If None, it will default to CameraNode.__camera_swidth__.
        @param sheight  The initial screen height (in pixels). If None, it will default to CameraNode.__camera_sheight__.
        @param parent   The parent SceneGraphItem instance.
        """
        super(GLCameraNode, self).__init__(position, target, up, fov, znear, zfar, swidth, sheight, parent)

    def resizeGL(self, width, height):
        """
        OpenGL Resize operation. Executes OpenGL logic during a resize callback.

        @param width The current width of the viewport.
        @param height The current height of the viewport.
        """
        GLNode.resizeGL(self, width, height)

        self.resize(width, height)

    def projectionGL(self):
        """
        OpenGL Viewport Projection operation. Execute any logic required to required by the Projection Matrix.
        """
        GLNode.projectionGL(self)

        GL.glFrustum(self._viewport[0], self._viewport[1], self._viewport[2], self._viewport[3], self._znear, self._zfar)

        self.transformation = Matrix4x4.lookAt(self._position, self._target, self._up, False)
        GL.glMultMatrixf(self.transformation.data)
