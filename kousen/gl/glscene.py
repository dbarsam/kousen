
from PySide import QtCore, QtGui
from OpenGL import GL
from OpenGL import GLU
from OpenGL import GLUT
from kousen.scenegraph import SceneGraphItem, SceneGraphModel
from kousen.gl.glutil import GLScope, GLVariableScope, GLAttribScope, GLClientAttribScope, GLMatrixScope

class GLNode(object):
    """
    The GLNode provide a base interface of OpenGL Scene Graph Node.
    """
    def __init__(self, *args, **kargs):
        """
        Constructor.

        @param args    The list of arguments to be passed along the constructor initialization chain.
        @param kargs   The list of key-word arguments to be passed along the constructor initialization chain.
        """
        super(GLNode, self).__init__(*args)

    def initializeGL(self):
        """
        OpenGL Initialization.  Execute any logic required during OpenGL initialization.
        """
        for child in self._children:
            child.initializeGL()

    def projectionGL(self):
        """
        OpenGL Viewport Projection operation. Execute any logic required to required by the Projection Matrix.
        """
        for child in self._children:
            child.projectionGL()

    def paintGL(self):
        """
        OpenGL Render operation.  Execute any logic required during the Draw callback.
        """
        for child in self._children:
            child.paintGL()

    def overlayGL(self):
        """
        OpenGL Overlay Render.  Execute any logic required during the 2-D Draw callback.
        """
        for child in self._children:
            child.overlayGL()

    def resizeGL(self, width, height):
        """
        OpenGL Resize operation. Executes OpenGL logic during a resize callback.

        @param width The current width of the viewport.
        @param height The current height of the viewport.
        """
        for child in self._children:
            child.resizeGL(width, height)


class GLSceneNode(GLNode, SceneGraphItem):
    """
    The GLSceneNode extends SceneGraphItem with the functionality of GLNode.
    """
    def __init__(self, sdata={}, parent=None):
        """
        Constructor.

        @param sdata   The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent  The initial parent GLSceneNode of this GLSceneNode
        """
        super(GLSceneNode, self).__init__(sdata, parent)

class GLSceneModel(SceneGraphModel):
    """
    The GLSceneModel provides a SceneGraphModel for GLSceneNodes.
    """
    def __init__(self, headerdata, parent=None):
        """
        Constructor.

        @param headerdata The initial instance of AbstractData or iterable object containing static data to be converted to an instance of AbstractData.
        @param parent     The initial QObject parent this GLSceneModel
        """
        super(GLSceneModel, self).__init__(headerdata, parent)
        self.rowsInserted.connect(self._rowsInserted)

    def _rowsInserted(self, parent, start, end):
        """
        Internal row inserted signal.
        """
        viewport = GL.glGetIntegerv( GL.GL_VIEWPORT )
        width    = viewport[2]
        height   = viewport[3]
        parentItem = self.item(parent)
        for row in range(start, end + 1):
            childItem = parentItem.child(row)
            childItem.initializeGL()
            childItem.resizeGL(width, height)
    
    def createRoot(self, *args):
        """
        Overrides the SceneGraphModel's createRoot method.

        @param   args A variable size list of arguments to be passed to the created root node.
        @returns      An instantiated GLSceneNode root node.
        """
        return GLSceneNode(*args)

    def createItem(self, *args):
        """
        Implements the SceneGraphModel's createItem method.

        @param   args A variable size list of arguments to be passed to the created node.
        @returns      An instantiated GLSceneNode node.
        """
        return GLSceneNode(*args)

    def initializeGL(self):
        """
        OpenGL Initialization.  Executes logic during an OpenGL context initialization.
        """
        GL.glClearColor(0.25, 0.28, 0.31, 1.0)
        GL.glClearDepth(1.0)

        # Polygon Rasterization
        GL.glPolygonMode( GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        
        # Polygon Anti-Aliasing
        GL.glEnable( GL.GL_POLYGON_SMOOTH )

        # Light Shading
        GL.glShadeModel( GL.GL_SMOOTH )

        # Enable Back Face Culling
        GL.glEnable( GL.GL_CULL_FACE )
        GL.glCullFace( GL.GL_BACK )

        # Enable Depth Testing
        GL.glEnable( GL.GL_DEPTH_TEST )
        GL.glDepthFunc( GL.GL_LEQUAL )
        GL.glDepthMask( GL.GL_TRUE )
        
        # Enable Lighting and Custom Lights
        GL.glEnable( GL.GL_LIGHTING )
        
        # Define Lights
        GL.glLightfv( GL.GL_LIGHT0, GL.GL_POSITION, [ 10.0, 10.0, 10.0, 1.0 ] )
        GL.glLightfv( GL.GL_LIGHT0, GL.GL_AMBIENT, [ 0.4, 0.4, 0.4, 1.0 ] )
        GL.glLightfv( GL.GL_LIGHT0, GL.GL_DIFFUSE, [ 0.4, 0.4, 0.4, 1.0 ] )
        GL.glLightfv( GL.GL_LIGHT0, GL.GL_SPECULAR, [ 1.0, 1.0, 1.0, 1.0 ] )
        GL.glEnable( GL.GL_LIGHT0 )
        
        # Misc
        GL.glDisable( GL.GL_FOG )
        GL.glDisable( GL.GL_TEXTURE_2D )

        self._root.initializeGL()

    def paintGL(self):
        """
        OpenGL Render operation.  Executes logic during an OpenGL context render paint operation.
        """
        with GLMatrixScope(GL.GL_PROJECTION, True):
            self._root.projectionGL()
            with GLMatrixScope(GL.GL_MODELVIEW, True):
                GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
                self._root.paintGL()

        self._root.overlayGL()

    def resizeGL(self, width, height):
        """
        OpenGL Resize operation. Executes OpenGL logic during a resize callback.

        @param width The current width of the viewport.
        @param height The current height of the viewport.
        """
        GL.glViewport(0, 0, width, height)
        self._root.resizeGL(width, height)
