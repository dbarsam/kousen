# -*- coding: utf-8 -*-
"""
This module provides the OpenGL specializations of an AbstractSceneGraphVisitor.
"""
from kousen.gl.glroot import GLNodeAdapter
from kousen.scenegraph.scene import AbstractSceneGraphVisitor

class GLInitializeVisitor(AbstractSceneGraphVisitor):
    """
    GLSceneGraphVisitor implementes a Scene Graph Traversal object in for an OpenGL Initialization operation
    """
    def __init__(self):
        super(GLInitializeVisitor, self).__init__()

    def _enter(self, node):
        """
        Overrides the AbstractSceneGraphVisitor's _enter method with OpenGL Initialization operations.

        @param node The current node in the traversal
        """
        adapter = GLNodeAdapter.adapter(node)
        if adapter:
            adapter.initialize_enter()              

    def _exit(self, node):
        """
        Overrides the AbstractSceneGraphVisitor's _exit method with OpenGL Initialization operations.

        @param node The current node in the traversal
        """
        adapter = GLNodeAdapter.adapter(node)
        if adapter:
            adapter.initialize_exit()

class GLResizeVisitor(AbstractSceneGraphVisitor):
    """
    GLSceneGraphVisitor implementes a Scene Graph Traversal object in for an OpenGL Resize operation
    """
    def __init__(self, width, height):
        """
        Constructor.

        @param width The current width of the viewport.
        @param height The current height of the viewport.
        """
        super(GLResizeVisitor, self).__init__()
        self._width = width
        self._height = height

    def _enter(self, node):
        """
        Overrides the AbstractSceneGraphVisitor's _enter method for an OpenGL Resize operation.

        @param node The current node in the traversal
        """
        adapter = GLNodeAdapter.adapter(node)
        if adapter:
            adapter.resize_enter(self._width, self._height)              

    def _exit(self, node):
        """
        Overrides the AbstractSceneGraphVisitor's _exit method for an OpenGL Resize operation.

        @param node The current node in the traversal
        """
        adapter = GLNodeAdapter.adapter(node)
        if adapter:
            adapter.resize_enter(self._width, self._height)

class GLPaintVisitor(AbstractSceneGraphVisitor):
    """
    GLSceneGraphVisitor implementes a Scene Graph Traversal object in for an OpenGL Paint operation
    """
    def __init__(self):
        """
        Constructor.

        @param width The current width of the viewport.
        @param height The current height of the viewport.
        """
        super(GLPaintVisitor, self).__init__()

    def _enter(self, node):
        """
        Overrides the AbstractSceneGraphVisitor's _enter method for an OpenGL Render operation.

        @param node The current node in the traversal
        """
        adapter = GLNodeAdapter.adapter(node)
        if adapter:
            adapter.paint_enter()

    def _exit(self, node):
        """
        Overrides the AbstractSceneGraphVisitor's _exit method for an OpenGL Render operation.

        @param node The current node in the traversal
        """
        adapter = GLNodeAdapter.adapter(node)
        if adapter:
            adapter.paint_exit()