from OpenGL import GL
from OpenGL import GLU
from PySide import QtCore
from PySide import QtGui

class Scope(object):
    """
    Scope provides a context manager base interface for various OpenGL operations.
    """
    def __init__(self):
        super(Scope, self).__init__()

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        return type

    def push(self):
        self.__enter__()

    def pop(self):
        self.__exit__(None, None, None)

class CompoundScope(Scope):
    """
    CompoundScope provides a context manager for a sequence of Scope objects.
    """
    def __init__(self, *args):
        super(Scope, self).__init__()
        self.__args = args
 
    def __enter__(self):
        for item in self.__args:
            item.__enter__()
 
    def __exit__(self, type, value, traceback):
        for item in reversed(self.args):
            item.__exit__(type, value, traceback)
        return type

class GLUQuadricScope(Scope):
    """
    GLUQuadricScope provides a context manager for a GLU.Quadric operations
    """
    def __init__(self):
        super(GLUQuadricScope, self).__init__()
        self._quadric = None

    def __enter__(self):
        if not self._quadric:
            self._quadric = GLU.gluNewQuadric()

    def __exit__(self ,type, value, traceback):
        if self._quadric:
            GLU.gluDeleteQuadric(_quadric);
            self._quadric = None
        return not type

class GLAttribScope(Scope):
    """
    GLAttribScope provides a context manager for an OpenGL Attribute operations (i.e. GL.glPushAttrib / GL.glPopAttrib)
    """
    def __init__(self, mask):
        super(GLAttribScope, self).__init__()
        self._mask = mask

    def __enter__(self):
        GL.glPushAttrib(self._mask)

    def __exit__(self ,type, value, traceback):
        GL.glPopAttrib()
        return not type

class GLClientAttribScope(Scope):
    """
    GLClientAttribScope provides a context manager for an OpenGL Client Attribute operations (i.e. GL.glPushClientAttrib / GL.glPushClientAttrib)
    """
    def __init__(self, mask):
        super(GLClientAttribScope, self).__init__()
        self._mask = mask

    def __enter__(self):
        GL.glPushClientAttrib(self._mask)

    def __exit__(self, type, value, traceback):
        GL.glPopClientAttrib()
        return not type

class GLMatrixScope(Scope):
    """
    GLClientAttribScope provides a context manager for an OpenGL Matrix Stack operations (i.e. GL.glPushMatrix / GL.glPopMatrix)
    """
    def __init__(self, matrixmode=None, identity=False):
        super(GLMatrixScope, self).__init__()
        self._nextmode = matrixmode
        self._identity = identity

    def __enter__(self):
        if self._nextmode:
            self._prevmode = GL.glGetIntegerv(GL.GL_MATRIX_MODE)
            GL.glMatrixMode(self._nextmode)
        GL.glPushMatrix();
        if self._identity:
            GL.glLoadIdentity()

    def __exit__(self ,type, value, traceback):
        GL.glPopMatrix()
        if self._nextmode:
            GL.glMatrixMode(self._prevmode)
        return not type

class GLVariableScope(Scope):
    """
    GLVariableScope provides a context manager for an OpenGL variable operations

        with GLVariableScope(GL.glLineWidth, GL.GL_LINE_WIDTH, 3.0):
        ...
    """
    def __init__(self, glmethod, glid, value):
        super(GLVariableScope, self).__init__()
        self._prevvalue = None
        self._nextvalue = value
        self._set = glmethod
        self._id = glid

    def __enter__(self):
        self._prevvalue = GL.glGetInteger(self._id)
        self._set(self._nextvalue)

    def __exit__(self ,type, value, traceback):
        self._set(self._prevvalue)
        return not type

class GLColorScope(Scope):
    """
    GLColorScope provides a context manager for an OpenGL glColor operations independent of the GL.GL_CURRENT_COLOR attribute.

        with GLColorScope(color):
        ...
    """
    def __init__(self, qcolor):
        super(GLColorScope, self).__init__()
        self._glcolor = None
        self._qcolor = None
        if isinstance(qcolor, QtGui.QColor):
            self._qcolor = qcolor
        elif isinstance(qcolor, QtCore.Qt.GlobalColor):
            self._qcolor = QtGui.QColor(qcolor)

    def __enter__(self):
        if not self._glcolor and self._qcolor:
            self._glcolor = GL.glGetFloatv(GL.GL_CURRENT_COLOR)
            GL.glColor(self._qcolor.getRgbF())

    def __exit__(self ,type, value, traceback):
        if self._glcolor:
            GL.glColor(self._glcolor)
            self._glcolor = None
        return not type

class GLScope(Scope):
    """
    GLScope provides a context manager for an OpenGL operations (GL.glBegin / GL.glEnd)

        with GLVariableScope(GL.glLineWidth, GL.GL_LINE_WIDTH, 3.0):
        ...
    """
    def __init__(self, mode):
        super(GLScope, self).__init__()
        self._mode = mode

    def __enter__(self):
        GL.glBegin(self._mode)

    def __exit__(self ,type, value, traceback):
        GL.glEnd()
        return not type

