# -*- coding: utf-8 -*-
"""
This module provides class defintions of OpenGL primitive node adapters.
"""
import array

from OpenGL import GL
from kousen.gl.glutil import GLScope
from kousen.gl.gladapter import GLNodeAdapter
from kousen.scenegraph import CubeNode, GridNode

class GLColorCubeAdapter(GLNodeAdapter):
    """
    The GLColorCubeAdapter implements a GLNodeAdapter for a CubeNode
    """
    # Additional Meta Information
    __node__ = CubeNode

    def __init__(self, node):
        """
        Constructor.

        @param node The adaptable node.
        """
        super(GLColorCubeAdapter, self).__init__(node)
        self.__vertices   = array.array('f' , [ i * (node.size / 2) for i in
                                              [-1 , -1 ,  1 ,
                                               -1 ,  1 ,  1 ,
                                                1 ,  1 ,  1 ,
                                                1 , -1 ,  1 ,
                                               -1 , -1 , -1 ,
                                               -1 ,  1 , -1 ,
                                                1 ,  1 , -1 ,
                                                1 , -1 , -1] ] )
        self.__colors     = array.array('f' , [ 0 ,  0 ,  0 ,
                                                1 ,  0 ,  1 ,
                                                1 ,  1 ,  0 ,
                                                1 ,  1 ,  0 ,
                                                0 ,  0 ,  1 ,
                                                1 ,  0 ,  1 ,
                                                1 ,  1 ,  1 ,
                                                0 ,  1 ,  1] )
        self.__colorindex = array.array('B' , [ 0 ,  3 ,  2 ,
                                                1 ,  2 ,  3 ,
                                                7 ,  6 ,  0 ,
                                                4 ,  7 ,  3 ,
                                                1 ,  2 ,  6 ,
                                                5 ,  4 ,  5 ,
                                                6 ,  7 ,  0 ,
                                                1 ,  5 ,  4] )

    def paint_enter(self):
        """
        Implements the GLNodeAdapter's paint_enter method for an OpenGL Render operation.
        """
        GL.glPushAttrib(GL.GL_ENABLE_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_LINE_BIT | GL.GL_CURRENT_BIT)
        GL.glDisable( GL.GL_LIGHTING )
        GL.glPushClientAttrib(GL.GL_CLIENT_VERTEX_ARRAY_BIT)
        GL.glEnableClientState( GL.GL_COLOR_ARRAY )
        GL.glEnableClientState( GL.GL_VERTEX_ARRAY )
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPushMatrix();
        GL.glMultMatrixf(self._node.matrix().data())

        GL.glColorPointer( 3, GL.GL_FLOAT, 0, self.__colors.tostring() )
        GL.glVertexPointer( 3, GL.GL_FLOAT, 0, self.__vertices.tostring() )
        GL.glDrawElements( GL.GL_QUADS, 24, GL.GL_UNSIGNED_BYTE, self.__colorindex.tostring( ) )

    def paint_exit(self):
        """
        Implements the GLNodeAdapter's paint_exit method for an OpenGL Render operation.
        """
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPopMatrix();

        GL.glPopClientAttrib();
        GL.glPopAttrib()

class GLGridAdapter(GLNodeAdapter):
    """
    The GLGridPlane implements a GLNodeAdapter for a PlaneNode
    """
    # Additional Meta Information
    __node__ = GridNode

    def __init__(self, node):
        """
        Constructor.

        @param node The adaptable node.
        """
        super(GLGridAdapter, self).__init__(node)

    def paint_enter(self):
        """
        Implements the GLNodeAdapter's paint_enter method for an OpenGL Render operation.
        """
        GL.glPushAttrib(GL.GL_ENABLE_BIT | GL.GL_LIGHTING_BIT | GL.GL_LINE_BIT | GL.GL_CURRENT_BIT)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPushMatrix();
        GL.glMultMatrixf(self._node.matrix().data())

        GL.glEnable( GL.GL_COLOR_MATERIAL )
        GL.glDisable( GL.GL_LIGHTING )
        #GL.glLineWidth(3)
        with GLScope( GL.GL_LINES ):
            s = self._node.spacing
            c = self._node.count/2*s
            i = -c
            while i <= c:
                GL.glColor(0.5, 0.5, 0.5)
                GL.glVertex3f(  i, 0.0,  -c);
                GL.glVertex3f(  i, 0.0,   c)
                GL.glVertex3f(  c, 0.0,   i);
                GL.glVertex3f( -c, 0.0,   i);
                i += s
            GL.glColor(0.0, 0.0, 0.0)
            GL.glVertex3f(0.0, 0.0,   -c);
            GL.glVertex3f(0.0, 0.0,    c);
            GL.glVertex3f( -c, 0.0,  0.0);
            GL.glVertex3f(  c, 0.0,  0.0)

    def paint_exit(self):
        """
        Implements the GLNodeAdapter's paint_exit method for an OpenGL Render operation.
        """
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPopMatrix();
        GL.glPopAttrib()
