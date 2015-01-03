# -*- coding: utf-8 -*-
"""
This module provides class defintions of OpenGL camera node adapters.
"""
from OpenGL import GL
from kousen.scenegraph import CameraNode
from kousen.gl.gladapter import GLNodeAdapter

class GLCameraAdapter(GLNodeAdapter):
    """
    The GLCameraAdapter implements a GLNodeAdapter for a CameraNode.
    """
    # Additional Meta Information
    __node__ = CameraNode

    def __init__(self, node):
        """
        Constructor.

        @param node The node we are adapting.
        """
        super(GLCameraAdapter, self).__init__(node)

    def resize_enter(self, width, height):
        """
        Implements the GLNodeAdapter's resize_enter method for an OpenGL Resize operation.

        @param width The current width of the viewport.
        @param height The current height of the viewport.
        """
        self._node.resize(width, height)

    def paint_enter(self):
        """
        Implements the GLNodeAdapter's paint_enter method for an OpenGL Render operation.
        """
        viewport = self._node.viewport
        znear = self._node.znear
        zfar = self._node.zfar
        matrix = self._node.projectionMatrix()            

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glFrustum(viewport[0], viewport[1], viewport[2], viewport[3], znear, zfar)
        GL.glMultMatrixf(matrix.data())

