# -*- coding: utf-8 -*-
import math
from PySide import QtGui, QtCore
from OpenGL import GL
from OpenGL import GLU
from OpenGL import GLUT
from kousen.scenegraph import CameraHUDNode
from kousen.math import Point3D, Vector3D, Matrix4x4
from kousen.gl.glscene import GLNode
from kousen.gl.glutil import GLUQuadricScope, GLScope, GLVariableScope, GLAttribScope, GLClientAttribScope, GLMatrixScope
from kousen.gl.glprimitive import QuadricGnomon

class GLCameraHUDNode(GLNode, CameraHUDNode):
    """
    The GL Camera HUD Node provides an OpenGL implementation of a CameraHUDNode.
    """
    def __init__(self, camera, parent=None):
        """
        Constructor.

        @param camera   An instance of CameraNode to monitor.
        @param parent   The parent SceneGraphItem instance.
        """
        super(GLCameraHUDNode, self).__init__(camera, parent)
        self._gnomon = QuadricGnomon(0.4, self)
             
    def paintGL(self):
        """
        OpenGL Render operation.  Executes logic during an OpenGL context render paint operation.
        """
        # Gnomon
        GL.glViewport(10,10,80,80)
        with GLAttribScope(GL.GL_CURRENT_BIT | GL.GL_LINE_BIT | GL.GL_DEPTH_BUFFER_BIT):
            GL.glDisable(GL.GL_LIGHTING)
            with GLMatrixScope(GL.GL_PROJECTION, True):
                GL.glOrtho(-0.5,0.5,-0.5,0.5,-1.0, 1.0)
                with GLMatrixScope(GL.GL_MODELVIEW, True):
                    m = self._camera.transformation.duplicate()
                    m[12] = 0.0
                    m[13] = 0.0
                    m[14] = 0.0
                    GL.glMultMatrixf(m.data);
                    self._gnomon.paintGL()

        GL.glViewport(0,0,self._right, self._bottom);

    def resizeGL(self, width, height):
        """
        OpenGL Resize operation. Executes OpenGL logic during a resize callback.

        @param width The current width of the viewport.
        @param height The current height of the viewport.
        """
        GLNode.resizeGL(self, width, height)

        self.resize(width, height)

