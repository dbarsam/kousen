# -*- coding: utf-8 -*-
from OpenGL import GL
from kousen.scenegraph import TransformationNode
from kousen.gl.gladapter import GLNodeAdapter

class GLTransformationNode(GLNodeAdapter):
    """
    The GLTransformationNode implements a GLNodeAdapter for a TransformationNode.
    """
    # Additional Meta Information
    __node__ = TransformationNode

    def __init__(self, node):
        """
        Constructor.

        @param node The node we are adapting.
        """
        super(GLTransformationNode, self).__init__(node)

    def paint_enter(self):
        """
        Implements the GLNodeAdapter's paint_enter method for an OpenGL Render operation.
        """
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPushMatrix();
        GL.glMultMatrixf(self._node.matrix().data())        

    def paint_exit(self):
        """
        Implements the GLNodeAdapter's paint_exit method for an OpenGL Render operation.
        """
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPopMatrix();