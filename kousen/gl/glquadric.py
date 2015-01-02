# -*- coding: utf-8 -*-
"""
This module provides an openal quadric specializations of primitive node adapters.
"""
import array
import copy
import math
from enum import IntEnum, unique
from PySide import QtCore, QtGui
from OpenGL import GL, GLU, GLUT
#from kousen.scenegraph import PrimitiveNode
from kousen.math import Point3D, Vector3D, Matrix4x4
from kousen.gl.glutil import GLScope, GLVariableScope, GLAttribScope, GLClientAttribScope, GLMatrixScope, GLColorScope
from kousen.gl.gladapter import GLNodeAdapter
from kousen.scenegraph import SphereNode, CubeNode, CylinderNode, ConeNode, PlaneNode, QuadricSphereNode, QuadricCylinderNode, QuadricConeNode, GridNode, QuadricArrowNode, QuadricGnomonNode
from kousen.math import Matrix4x4

"""
http://stackoverflow.com/questions/8329546/how-to-use-vertex-buffer-objects-vbo-instead-of-calling-gldrawarrays-thousands
en.wikibooks.org/wiki/OpenGL_Programming/Scientific_OpenGL_Tutorial_04
"""
class GLQuadricSphereAdapter(GLNodeAdapter):
    """
    The GLQuadricSphereAdapter implements a GLNodeAdapter for a SphereNode
    """
    # Additional Meta Information
    __node__ = QuadricSphereNode

    def __init__(self, node):
        """
        Constructor.

        @param radius   The radius of the sphere.
        @param parent   The parent SceneGraphNode instance.
        """
        super(GLQuadricSphereAdapter, self).__init__(node)
        self.__quadric = GLU.gluNewQuadric()

    def paint_enter(self):
        """
        Implements the GLNodeAdapter's paint_enter method for an OpenGL Render operation.
        """
        GL.glPushAttrib(GL.GL_ENABLE_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_LINE_BIT | GL.GL_CURRENT_BIT)
        GL.glPushClientAttrib(GL.GL_CLIENT_VERTEX_ARRAY_BIT)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPushMatrix()
        GL.glMultMatrixf(self._node.matrix().data())
        GL.glColor(self._node.color.getRgbF())

        q = self.__quadric
        r = self._node.radius
        sl = self._node.slices
        st = self._node.stacks
        GLU.gluQuadricNormals(q, GLU.GLU_SMOOTH )
        GLU.gluQuadricDrawStyle(q, GLU.GLU_FILL );
        GLU.gluSphere(q, r, sl, st)

    def paint_exit(self):
        """
        Implements the GLNodeAdapter's paint_exit method for an OpenGL Render operation.
        """
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPopMatrix()
        GL.glPopClientAttrib();
        GL.glPopAttrib()

#class GLQuadricArrowAdapter(GLNodeAdapter):
#    """
#    The GLQuadricCylinderAdapter implements a GLNodeAdapter for a CylinderNode
#    """
#    # Additional Meta Information
#    __node__ = QuadricArrowNode

#    def paint_enter(self):
#        """
#        Implements the GLNodeAdapter's paint_enter method for an OpenGL Render operation.
#        """
#        GL.glMatrixMode(GL.GL_MODELVIEW)
#        GL.glPushMatrix();        
#        GL.glMultMatrixf(self._node.matrix().data())

#    def paint_exit(self):
#        """
#        Implements the GLNodeAdapter's paint_exit method for an OpenGL Render operation.
#        """
#        GL.glMatrixMode(GL.GL_MODELVIEW)
#        GL.glPopMatrix()

class GLGnomonAdapter(GLNodeAdapter):
    """
    The GLGnomonAdapter implements a GLNodeAdapter for a QuadricGnomonNode
    """
    # Additional Meta Information
    __node__ = QuadricGnomonNode

    def __init__(self, node):
        """
        Constructor.

        @param node The adaptable node.
        """
        super(GLGnomonAdapter, self).__init__(node)

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
        with GLAttribScope(GL.GL_ENABLE_BIT | GL.GL_CURRENT_BIT):
            with GLColorScope( QtCore.Qt.GlobalColor.white ):
                GL.glDisable(GL.GL_DEPTH_TEST)

                GL.glRasterPos3fv(self._node.xaxis.data())
                GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_12, ord('X'))

                GL.glRasterPos3fv(self._node.yaxis.data())
                GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_12, ord('Y'))
                
                GL.glRasterPos3fv(self._node.zaxis.data())
                GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_12, ord('Z'))

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPopMatrix()

class GLQuadricCylinderAdapter(GLNodeAdapter):
    """
    The GLQuadricCylinderAdapter implements a GLNodeAdapter for a CylinderNode
    """
    # Additional Meta Information
    __node__ = QuadricCylinderNode

    def __init__(self, node):
        """
        Constructor.

        @param node The adaptable node.
        """
        super(GLQuadricCylinderAdapter, self).__init__(node)
        self.__quadric = GLU.gluNewQuadric()

    @staticmethod
    def _glcylinder(quadric, radius, height, slices, stacks, loops):
        """
        Internal method to render a quadric cylinder with OpenGL commands

        @param quadric  The OpenGL quadric object
        @param radius   The radius of the cylinder's base.
        @param height   The height of the cylunder.
        @param slices   The number of subdivisions around the z-axis (similar to lines of longitude).
        @param stacks   The number of subdivisions along the z-axis (similar to lines of latitude).
        @param loops    The number of concentric rings about the origin into which the cylinder's base is subdivided.
        """
        GLU.gluCylinder(quadric, radius, radius, height, slices, stacks)

        # The positive Z-axis is the default direction fo Cylinder Quadrics in OpenGL.
        # The top disc is 'height' units away from the origin.
        with GLMatrixScope(GL.GL_MODELVIEW, False):        
            GL.glTranslate(0, 0, height);
            GLU.gluDisk(quadric, 0.0, radius, slices, loops)
        
        # The positive Z-axis is the default direction for Cylinder Quadrics in OpenGL.
        # The base disc renders at the origin, but must be rotated to face the opposite
        # along the negative z axis.
        with GLMatrixScope(GL.GL_MODELVIEW, False):        
            GL.glRotate(180, 0, 1, 0)
            GLU.gluDisk(quadric, 0.0, radius, slices, loops)

    def paint_enter(self):
        """
        Implements the GLNodeAdapter's paint_enter method for an OpenGL Render operation.
        """
        GL.glPushAttrib(GL.GL_ENABLE_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_LINE_BIT | GL.GL_CURRENT_BIT)
        GL.glPushClientAttrib(GL.GL_CLIENT_VERTEX_ARRAY_BIT)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPushMatrix()
        GL.glMultMatrixf(self._node.matrix().data())
        GL.glColor(self._node.color.getRgbF())
        

        # The positive Z-axis is the default direction for Cylinder Quadrics in OpenGL.
        # If our vector is not parallel to the z-axis, e.g. (0, 0, Z), then rotate it.
        #   1) Get a normal from the z-v plane
        #   2) Get the angle inbetween z-v on the plane (see vector dot product)
        #   3) Rotate the normal by that angle.
        v = self._node.axis
        m = Matrix4x4.identity()
        if v.x != 0 or v.y != 0:
            zaxis  = Vector3D(0,0,1)
            angle  = zaxis.angle(v)
            normal = zaxis.crossproduct(v, True)
            m *= Matrix4x4.rotation(angle, normal)

        # The positive Z-axis is the default direction fo Cylinder Quadrics in OpenGL.
        # If our z is negative, we need to flip the cylinder
        if v.z < 0:
            yaxis  = Vector3D(1,0,0)
            m *= Matrix4x4.rotation(math.radians(180), yaxis)       
        GL.glMultMatrixf(m.data())

        q = self.__quadric
        r = self._node.radius
        h = self._node.length
        sl = self._node.slices
        st = self._node.stacks
        lp = self._node.loops
        GLU.gluQuadricDrawStyle (q, GLU.GLU_FILL)
        GLU.gluQuadricNormals (q, GLU.GLU_SMOOTH)
        GLU.gluQuadricOrientation(q, GLU.GLU_OUTSIDE)
        self._glcylinder(q, r, h, sl, st, lp)

    def paint_exit(self):
        """
        Implements the GLNodeAdapter's paint_exit method for an OpenGL Render operation.
        """
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPopMatrix()
        GL.glPopClientAttrib();
        GL.glPopAttrib()

class GLQuadricConeAdapter(GLQuadricCylinderAdapter):
    """
    The GLQuadricConeAdapter implements a specialized GLQuadricCylinderAdapter for a QuadricConeNode
    """
    # Additional Meta Information
    __node__ = QuadricConeNode

    @staticmethod
    def _glcylinder(quadric, radius, height, slices, stacks, loops):
        """
        Internal method to render a quadric cylinder with OpenGL commands

        @param quadric  The OpenGL quadric object
        @param radius   The radius of the cylinder's base.
        @param height   The height of the cylunder.
        @param slices   The number of subdivisions around the z-axis (similar to lines of longitude).
        @param stacks   The number of subdivisions along the z-axis (similar to lines of latitude).
        @param loops    The number of concentric rings about the origin into which the cylinder's base is subdivided.
        """
        GLU.gluCylinder(quadric, radius, 0, height, slices, stacks)
        
        # The positive Z-axis is the default direction for Cylinder Quadrics in OpenGL.
        # The base disc renders at the origin, but must be rotated to face the opposite along the negative z axis.
        with GLMatrixScope(GL.GL_MODELVIEW, False):        
            GL.glRotate(180, 0, 1, 0)
            GLU.gluDisk(quadric, 0.0, radius, slices, loops)
