import inspect

class GLNodeAdapter(object):
    """
    The GLNodeAdapter implements an OpenGL adapter interface for an node.
    """
    _nodemap = {}

    def __init__(self, node):
        """
        Constructor.

        @param node The node we are adapting.
        """
        super(GLNodeAdapter, self).__init__()
        self._node = node

    @classmethod
    def adapter(cls, node):
        """
        Returns the best matched GLNodeAdapter-derived class for a node.
        """
        nodename = node.__class__.__name__
        adapter = cls._nodemap.get(nodename, None)

        if not adapter:
            # If there is no adapter, find an adapter for the node by finding
            # the first matching adapter in a traversal of the node's class
            # hierarchy.
            for subnodename in [c.__name__ for c in node.baseclasses()]:
                adapter = next((c for c in cls.subclasses() if c.__node__.__name__ == subnodename), None)
                if adapter:
                    cls._nodemap[nodename] = adapter
                    break
        if not adapter:
            raise Exception("Unable to resolve an adapter for node {0}".format(str(node)))
        return adapter(node)

    @classmethod
    def subclasses(cls, recursive = True):
        """
        Calculates all derived subclasses.

        @param   recursive True if the subclass search should recusively delve into the inheritance tree.
        @returns           A list of GLNodeAdapter-derived class type.
        """
        sb = cls.__subclasses__()
        if recursive:
            for c in cls.__subclasses__():
                sb.extend(c.subclasses())
        return sb

    def initialize_enter(self):
        """
        Enter OpenGL Initialization.  Execute any logic required during an OpenGL initialization but before processing additional nodes.
        """
        pass

    def initialize_exit(self):
        """
        Exit OpenGL Initialization.  Execute any logic required during an OpenGL initialization but after processing additional nodes.
        """
        pass

    def resize_enter(self, width, height):
        """
        Enter OpenGL Resize operation.  Execute any logic required during an OpenGL resize operation but before processing additional nodes.

        @param width The current width of the viewport.
        @param height The current height of the viewport.
        """
        pass

    def resize_exit(self, width, height):
        """
        Exit OpenGL Resize operation.  Execute any logic required during an OpenGL resize operation but after processing additional nodes.

        @param width The current width of the viewport.
        @param height The current height of the viewport.
        """
        pass

    def paint_enter(self):
        """
        Enter OpenGL Render operation.  Execute any logic required during OpenGL redering but before processing additional nodes.
        """
        pass

    def paint_exit(self):
        """
        Exit OpenGL Render operation.  Execute any logic required during OpenGL redering but after processing additional nodes.
        """
        pass