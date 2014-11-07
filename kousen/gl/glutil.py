from OpenGL import GL
from OpenGL import GLU

class GLUQuadricScope(object):
    """
    GLUQuadricScope provides a context manager for a GLU.Quadric operations
    """
    def __init__(self):
        pass

    def __enter__(self):
        self._quadric = quadric = GLU.gluNewQuadric()

    def __exit__(self ,type, value, traceback):
        if self._quadric:
            GLU.gluDeleteQuadric(_quadric);
        return not type

class GLAttribScope(object):
    """
    GLAttribScope provides a context manager for an OpenGL Attribute operations (i.e. GL.glPushAttrib / GL.glPopAttrib)
    """
    def __init__(self, mask):
        self._mask = mask

    def __enter__(self):
        GL.glPushAttrib(self._mask)

    def __exit__(self ,type, value, traceback):
        GL.glPopAttrib()
        return not type

class GLClientAttribScope(object):
    """
    GLClientAttribScope provides a context manager for an OpenGL Client Attribute operations (i.e. GL.glPushClientAttrib / GL.glPushClientAttrib)
    """
    def __init__(self, mask):
        self._mask = mask

    def __enter__(self):
        GL.glPushClientAttrib(self._mask)

    def __exit__(self, type, value, traceback):
        GL.glPopClientAttrib()
        return not type

class GLMatrixScope(object):
    """
    GLClientAttribScope provides a context manager for an OpenGL Matrix Stack operations (i.e. GL.glPushMatrix / GL.glPopMatrix)
    """
    def __init__(self, matrixmode=None, identity=False):
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

class GLVariableScope(object):
    """
    GLVariableScope provides a context manager for an OpenGL variable operations

        with GLVariableScope(GL.glLineWidth, GL.GL_LINE_WIDTH, 3.0):
        ...
    """
    def __init__(self, glmethod, glid, value):
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

class GLScope(object):
    """
    GLScope provides a context manager for an OpenGL operations (GL.glBegin / GL.glEnd)

        with GLVariableScope(GL.glLineWidth, GL.GL_LINE_WIDTH, 3.0):
        ...
    """
    def __init__(self, mode):
        self._mode = mode

    def __enter__(self):
        GL.glBegin(self._mode)

    def __exit__(self ,type, value, traceback):
        GL.glEnd()
        return not type
