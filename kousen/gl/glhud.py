# -*- coding: utf-8 -*-
"""
This module provides class defintions of OpenGL HUD node adapters.
"""
from OpenGL import GL
from kousen.scenegraph import CameraHUDNode
from kousen.gl.gladapter import GLNodeAdapter

class GLCameraHUDAdapter(GLNodeAdapter):
    """
    The GLCameraHUDAdapter implements a GLNodeAdapter for a CameraHUDNode.
    """
    # Additional Meta Information
    __node__ = CameraHUDNode

    def __init__(self, node):
        """
        Constructor.

        @param node The node we are adapting.
        """
        super(GLCameraHUDAdapter, self).__init__(node)

    def reesize_enter(self, width, height):
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
        if self._node.camera:
            GL.glPushAttrib(GL.GL_VIEWPORT_BIT | GL.GL_ENABLE_BIT)
            GL.glMatrixMode(GL.GL_PROJECTION)
            GL.glPushMatrix();
            GL.glLoadIdentity()
            
            GL.glDisable(GL.GL_LIGHTING)
            GL.glViewport(10,10,80,80)               
            GL.glOrtho(-0.5,0.5,-0.5,0.5,-1.0, 1.0)

            # Extract the current transformation matrix but remove the translation
            m = self._node.camera.projectionMatrix().duplicate()
            m[12] = 0.0
            m[13] = 0.0
            m[14] = 0.0                
            GL.glMatrixMode(GL.GL_MODELVIEW)
            GL.glPushMatrix();
            GL.glLoadMatrixf(m.data());

    def paint_exit(self):
        """
        Implements the GLNodeAdapter's paint_exit method for an OpenGL Render operation.
        """
        if self._node.camera:
            GL.glMatrixMode(GL.GL_MODELVIEW)
            GL.glPopMatrix();
        
            GL.glMatrixMode(GL.GL_PROJECTION)
            GL.glPopMatrix();

            GL.glPopAttrib()
