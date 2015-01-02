from OpenGL import GL
from OpenGL import GLU

from kousen.gl.gladapter import GLNodeAdapter
from kousen.gl.glutil import GLUQuadricScope, GLScope, GLVariableScope, GLAttribScope, GLClientAttribScope, GLMatrixScope
from kousen.scenegraph.scene import SceneGraphRoot

class GLRootAdapter(GLNodeAdapter):
    """
    The GLRootAdapter implements a GLNodeAdapter for a SceneGraphRoot
    """
    # Additional Meta Information
    __node__ = SceneGraphRoot

    def __init__(self, node):
        """
        Constructor.

        @param node The adaptable node.
        """
        super(GLRootAdapter, self).__init__(node)

    def initialize_enter(self):
        """
        Implements the GLNodeAdapter's initialize_enter method for an OpenGL Initialization operation.
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

        # Misc
        GL.glDisable( GL.GL_FOG )
        GL.glDisable( GL.GL_TEXTURE_2D )

    def resize_enter(self, width, height):
        """
        Implements the GLNodeAdapter's resize_enter method for an OpenGL Resize operation.

        @param width The current width of the viewport.
        @param height The current height of the viewport.
        """
        GL.glViewport(0, 0, width, height)

    def paint_enter(self):
        """
        Implements the GLNodeAdapter's paint_enter method for an OpenGL Render operation.
        """
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
