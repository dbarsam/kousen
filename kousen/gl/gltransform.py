from PySide import QtCore, QtGui
from OpenGL import GL
from OpenGL import GLU
from kousen.math import Matrix4x4
from kousen.gl.glscene import GLNode
from kousen.scenegraph import TranslationNode, RotationNode, ScaleNode

class GLTransformationNode(GLNode):
    """
    The GLTransformationNode provide a base interface of OpenGL Scene Graph Transformation Node.
    """
    def __init__(self, *args, **kargs):
        """
        Constructor.

        @param args    The list of arguments to be passed along the constructor initialization chain.
        @param kargs   The list of key-word arguments to be passed along the constructor initialization chain.
        """
        super(GLTransformationNode, self).__init__(*args, **kwargs)

    def paintGL(self):
        """
        OpenGL Render operation.  Executes logic during an OpenGL context render paint operation.
        """
        GL.glPushMatrix()
        GL.glMultMatrixf(self._matrix.data)

        super(GLTransformationNode, self).paintGL()

        GL.glPopMatrix()

class GLTranslationNode(GLTransformationNode, TranslationNode):
    """
    GLTranslationNode extens the TranslationNode with OpenGL Functionality
    """
    # Additional Meta Information
    __category__     = "OpenGL Transformation Node"
    __description__  = "Translation Node"
    __instantiable__ = True

    def __init__(self, translation, sdata={}, parent=None):
        """
        Constructor.

        @param translation The initial translation vector.
        @param sdata       The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent      The initial parent SceneGraphItem of this SceneGraphItem
        """
        super(GLTranslationNode, self).__init__(translation, sdata, parent)

class GLRotationNode(GLTransformationNode, RotationNode):
    """
    GLRotationNode extens the RotationNode with OpenGL Functionality
    """
    # Additional Meta Information
    __category__     = "OpenGL Transformation Node"
    __description__  = "Rotation Node"
    __instantiable__ = True

    def __init__(self, angle, axis, point, sdata={}, parent=None):
        """
        Constructor.

        @param angle   The initial rotation angle (radians).
        @param axis    The initial rotation axis.
        @param point   The initial rotation origin point.
        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial parent SceneGraphItem of this SceneGraphItem
        """
        super(GLSceneNode, self).__init__(angle, axis, point, sdata, parent)

class GLScaleNode(GLTransformationNode, ScaleNode):
    """
    GLScaleNode extens the ScaleNode with OpenGL Functionality
    """
    # Additional Meta Information
    __category__     = "OpenGL Transformation Node"
    __description__  = "Scale Node"
    __instantiable__ = True

    def __init__(self, factor, point, data={}, parent=None):
        """
        Constructor.

        @param factor  The initial scale factor.
        @param point   The initial scale origin point.
        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial parent SceneGraphItem of this SceneGraphItem
        """
        super(GLSceneNode, self).__init__(factor, point, data, parent)
