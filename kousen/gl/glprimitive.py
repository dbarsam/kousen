# -*- coding: utf-8 -*-
import array
import copy
import math
from PySide import QtCore, QtGui
from OpenGL import GL, GLU, GLUT
from kousen.scenegraph import PrimitiveNode
from kousen.math import Point3D, Vector3D, Matrix4x4
from kousen.gl.glutil import GLScope, GLVariableScope, GLAttribScope, GLClientAttribScope, GLMatrixScope
from kousen.gl.glscene import GLSceneNode
from kousen.gl.glscene import GLNode
from kousen.scenegraph import CameraNode
from kousen.math import Matrix4x4

class GLPrimitiveNode(GLNode, PrimitiveNode):
    """
    Base class for any Primitive used in the GLWidget class.
    """
    # Additional Meta Information
    __primitive_selectioncolor__ = QtGui.QColor(255, 0, 0)

    # Additional Meta Information
    __category__ = "OpenGL Primitive"

    def __init__(self, name, parent=None):
        """
        Constructor.

        @param name     The label of this object node.
        @param parent   The parent SceneGraphNode instance.
        """
        super(GLPrimitiveNode, self).__init__(name, parent)

        # Initial color of the object.
        self.__color = QtGui.QColor(0, 255, 0)
        self._selected = False

    @property
    def selected(self):
        """
        Convenience property to access the selection state of the node.

        @returns True if the object is selected; False otherwise.
        """
        return self._selected

    @selected.setter
    def selected(self, value):
        """
        Convenience property to access the selection state of the node.

        @param value True if the object is to be selected; False otherwise.
        """
        self._selected = value

    @property
    def color(self):
        """
        Convenience property to access the color state node.

        @returns A QtGui.QColor instance.
        """
        if self._selected:
            return self.__primitive_selectioncolor__
        return self.__color

    @color.setter
    def color(self, value):
        """
        Convenience property to access the color state node.

        @param value A QtGui.QColor instance.
        """
        self.__color = value

    def _prepaintGL(self):
        """
        Internal OpenGL Render operation.  Execute any logic required before the Draw callback.
        """
        super(GLPrimitiveNode, self)._prepaintGL()

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPushMatrix();

        GL.glMultMatrixf(self.matrix().data())

    def _postpaintGL(self):
        """
        Internal OpenGL Render operation.  Execute any logic required after the Draw callback.
        """
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPopMatrix();

        super(GLPrimitiveNode, self)._postpaintGL()

class GridObject(GLPrimitiveNode):

    __description__  = "Grid Primitve"
    __instantiable__ = True

    def __init__(self, count = 14, space = 0.5, parent=None):
        """
        Constructor.

        @param count    The number of lines in the grid.
        @param space    The spaceing between lines.
        @param parent   The parent SceneGraphNode instance.
        """
        super(GridObject, self).__init__(self.__description__, parent)
        self.__spacing = space
        self.__count = count

    def _paintGL(self):
        """
        OpenGL Render operation.  Executes logic during an OpenGL context render paint operation.
        """
        super(GridObject, self)._paintGL()

        with GLAttribScope(GL.GL_ENABLE_BIT | GL.GL_LIGHTING_BIT | GL.GL_LINE_BIT | GL.GL_CURRENT_BIT):
            with GLMatrixScope(GL.GL_MODELVIEW, False):
                GL.glEnable( GL.GL_COLOR_MATERIAL )
                GL.glDisable( GL.GL_LIGHTING )
                with GLScope( GL.GL_LINES ):
                    s = self.__spacing
                    c = self.__count/2*self.__spacing
                    i = -c
                    while i <= c:
                        GL.glColor(0.5, 0.5, 0.5)
                        GL.glVertex3f(  i, 0.0,  -c);
                        GL.glVertex3f(  i, 0.0,   c)
                        GL.glVertex3f(  c, 0.0,   i);
                        GL.glVertex3f( -c, 0.0,   i);
                        i += self.__spacing
                    GL.glColor(0.0, 0.0, 0.0)
                    GL.glVertex3f(0.0, 0.0,   -c);
                    GL.glVertex3f(0.0, 0.0,    c);
                    GL.glVertex3f( -c, 0.0,  0.0);
                    GL.glVertex3f(  c, 0.0,  0.0)


class QuadricArrow(GLPrimitiveNode):

    __description__  = "Arrow Primitve"
    __instantiable__ = True

    def __init__(self, head = Point3D(0,1,0), tail = Point3D(0,0,0), cyradius = 0.005, coradius = 0.075, mid=0.80, parent=None):
        """
        Constructor.

        @param head The point representing the tip of the arrow
        @param tail The point representing the base of the arrow
        @param cyradius The radius of the cylinder used in the arrow shaft
        @param coradius The radius of the cone used in the arrow tip
        @param mid      The "mid point" or the percentage [0,1] along the length where the cylinder and cone join
        @param parent   The parent SceneGraphNode instance.
        """
        super(QuadricArrow, self).__init__(self.__description__, parent)

        vector       = head - tail
        length       = vector.length()

        self.__cyradius     = cyradius
        self.__cyheight     = length  * mid
        self.__coradius     = coradius
        self.__coheight     = length - self.__cyheight

        # The arrow starts at the base point and points to the head.
        self.__transformation = Matrix4x4.translation(tail)

        # The positive Z-axis is the default direction fo Cylinder Quadrics in OpenGL.
        # If our vector is not parallel to the z-axis, e.g. (0, 0, Z), then rotate it.
        #   1) Get a normal from the z-v plane
        #   2) Get the angle inbetween z-v on the plane (see vector dot product)
        #   3) Rotate the normal by that angle.
        if not(vector.x == 0 and vector.y == 0):
            zaxis  = Vector3D(0,0,1)
            angle  = zaxis.angle(vector)
            normal = zaxis.crossproduct(vector, True)
            self.__transformation *= Matrix4x4.rotation(angle, normal)

        # The positive Z-axis is the default direction fo Cylinder Quadrics in OpenGL.
        # If our z is negative, we need to flip the arrow
        if vector.z < 0:
            yaxis  = Vector3D(1,0,0)
            self.__transformation *= Matrix4x4.rotation(math.radians(180), yaxis)


    def _paintGL(self):
        """
        OpenGL Render operation.  Executes logic during an OpenGL context render paint operation.
        """
        super(QuadricArrow, self)._paintGL()

        with GLMatrixScope():
            GL.glMultMatrixf(self.__transformation.data())

            #Arrow Shaft
            quadric = GLU.gluNewQuadric()
            GLU.gluQuadricDrawStyle (quadric, GLU.GLU_FILL);
            GLU.gluQuadricNormals (quadric, GLU.GLU_SMOOTH);
            GLU.gluCylinder(quadric, self.__cyradius, self.__cyradius, self.__cyheight, 32, 1);

            quadric = GLU.gluNewQuadric()
            GLU.gluQuadricOrientation(quadric, GLU.GLU_INSIDE)
            GLU.gluQuadricDrawStyle(quadric, GLU.GLU_FILL);
            GLU.gluQuadricNormals(quadric, GLU.GLU_SMOOTH);
            GLU.gluDisk(quadric, 0.0, self.__cyradius, 32, 1);

            # Arrow Tip
            GL.glTranslate(0, 0, self.__cyheight);
            quadric = GLU.gluNewQuadric()
            GLU.gluQuadricDrawStyle(quadric, GLU.GLU_FILL);
            GLU.gluQuadricNormals(quadric, GLU.GLU_SMOOTH);
            GLU.gluCylinder(quadric, self.__coradius, 0.0, self.__coheight, 32, 1);

            quadric = GLU.gluNewQuadric()
            GLU.gluQuadricOrientation(quadric, GLU.GLU_INSIDE)
            GLU.gluQuadricDrawStyle(quadric, GLU.GLU_FILL);
            GLU.gluQuadricNormals(quadric, GLU.GLU_SMOOTH);
            GLU.gluDisk(quadric, 0.0, self.__coradius, 32, 1);


class QuadricSphere(GLPrimitiveNode):

    __description__  = "Sphere Primitve"
    __instantiable__ = True

    def __init__(self, radius = 1.0, parent=None):
        """
        Constructor.

        @param radius   The radius of the sphere.
        @param parent   The parent SceneGraphNode instance.
        """
        super(QuadricSphere, self).__init__(self.__description__, parent)
        self.__radius = radius
        self.__quadric = GLU.gluNewQuadric()

    def _paintGL(self):
        """
        OpenGL Render operation.  Executes logic during an OpenGL context render paint operation.
        """
        super(QuadricSphere, self)._paintGL()

        with GLAttribScope(GL.GL_ENABLE_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_LINE_BIT | GL.GL_CURRENT_BIT):
            with GLClientAttribScope(GL.GL_CLIENT_VERTEX_ARRAY_BIT):
                with GLMatrixScope(GL.GL_MODELVIEW, False):
                    q = self.__quadric
                    GLU.gluQuadricNormals(q, GLU.GLU_SMOOTH )
                    GLU.gluQuadricDrawStyle( q, GLU.GLU_FILL );
                    GLU.gluSphere(q, self.__radius, 32, 32)

class ColorCubeObject(GLPrimitiveNode):

    __description__  = "Color Cube Primitve"
    __instantiable__ = True

    def __init__(self, length = 1.0, parent=None):
        """
        Constructor.

        @param length   The length of one dimension of the cube.
        @param parent   The parent SceneGraphNode instance.
        """
        super(ColorCubeObject, self).__init__(self.__description__, parent)
        self.__length = length
        self.__vertices   = array.array('f' , [ i * (length / 2) for i in
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

    def _paintGL(self):
        """
        OpenGL Render operation.  Executes logic during an OpenGL context render paint operation.
        """
        super(ColorCubeObject, self)._paintGL()

        with GLAttribScope(GL.GL_ENABLE_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_LINE_BIT | GL.GL_CURRENT_BIT):
            with GLClientAttribScope(GL.GL_CLIENT_VERTEX_ARRAY_BIT):
                with GLMatrixScope(GL.GL_MODELVIEW, False):
                    GL.glDisable( GL.GL_LIGHTING )
                    GL.glEnableClientState( GL.GL_COLOR_ARRAY )
                    GL.glEnableClientState( GL.GL_VERTEX_ARRAY )
                    GL.glColorPointer( 3, GL.GL_FLOAT, 0, self.__colors.tostring() )
                    GL.glVertexPointer( 3, GL.GL_FLOAT, 0, self.__vertices.tostring() )
                    GL.glDrawElements( GL.GL_QUADS, 24, GL.GL_UNSIGNED_BYTE, self.__colorindex.tostring( ) )

class QuadricGnomon(GLPrimitiveNode):

    __description__  = "Gnomon Primitive"
    __instantiable__ = False

    def __init__(self, length = 0.4, parent=None):
        """
        Constructor.

        @param length   The length of the individal arrows of the gnomon.
        @param parent   The parent SceneGraphNode instance.
        """
        super(QuadricGnomon, self).__init__(self.__description__, parent)

        self.__o = Vector3D();
        self.__x = Vector3D(length, 0, 0)
        self.__y = Vector3D(0, length, 0)
        self.__z = Vector3D(0, 0, length)

        self.__xarrow = QuadricArrow(self.__x, self.__o, 0.005, 0.05, 0.80, self)
        self.__yarrow = QuadricArrow(self.__y, self.__o, 0.005, 0.05, 0.80, self)
        self.__zarrow = QuadricArrow(self.__z, self.__o, 0.005, 0.05, 0.80, self)

    def _paintGL(self):
        """
        OpenGL Render operation.  Executes logic during an OpenGL context render paint operation.
        """
        super(QuadricGnomon, self)._paintGL()

        with GLAttribScope(GL.GL_ENABLE_BIT | GL.GL_DEPTH_BUFFER_BIT | GL.GL_LINE_BIT | GL.GL_CURRENT_BIT):
            with GLClientAttribScope(GL.GL_CLIENT_VERTEX_ARRAY_BIT):
                with GLMatrixScope(GL.GL_MODELVIEW, False):

                    with GLMatrixScope(GL.GL_MODELVIEW, False):
                        GL.glColor(1, 0, 0)
                        self.__xarrow.paintGL()

                    with GLMatrixScope(GL.GL_MODELVIEW, False):
                        GL.glColor(0, 1, 0)
                        self.__yarrow.paintGL()

                    with GLMatrixScope(GL.GL_MODELVIEW, False):
                        GL.glColor(0, 0, 1)
                        self.__zarrow.paintGL()

                    # Axes labels
                    GL.glDisable(GL.GL_DEPTH_TEST)
                    GL.glColor(1, 1, 1)
                    GL.glRasterPos3fv(self.__x.data())
                    GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_12, ord('X'))
                    GL.glRasterPos3fv(self.__y.data())
                    GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_12, ord('Y'))
                    GL.glRasterPos3fv(self.__z.data())
                    GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_12, ord('Z'))
