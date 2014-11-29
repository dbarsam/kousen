# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
from OpenGL import GL
from OpenGL import GLU
from kousen.math import Matrix4x4
from kousen.gl.glscene import GLNode
from kousen.scenegraph.transform import TransformationNode

class GLTransformationNode(GLNode, TransformationNode):
    """
    The GLTransformationNode extends TransformationNode with the functionality of GLNode.
    """
    # Additional Meta Information
    __category__     = "OpenGL Transformation Node"
    __description__  = "Transformation Node"
    __instantiable__ = True

    def __init__(self, name, parent=None):
        """
        Constructor.

        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial parent GLSceneNode of this GLTransformationNode
        """
        super(GLTransformationNode, self).__init__(name, parent)

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

#class GLTransformationNode(GLNode, SceneGraphNode):
#    """
#    The GLTransformationNode provide a base interface of OpenGL Scene Graph Transformation Node.
#    """
#    def __init__(self, *args, **kargs):
#        """
#        Constructor.

#        @param args    The list of arguments to be passed along the constructor initialization chain.
#        @param kargs   The list of key-word arguments to be passed along the constructor initialization chain.
#        """
#        super(GLTransformationNode, self).__init__(*args, **kwargs)

#    def paintGL(self):
#        """
#        OpenGL Render operation.  Executes logic during an OpenGL context render paint operation.
#        """
#        GL.glPushMatrix()
#        GL.glMultMatrixf(self._matrix.data())

#        super(GLTransformationNode, self).paintGL()

#        GL.glPopMatrix()


