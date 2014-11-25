from PySide import QtCore, QtGui, QtOpenGL

class GLWidget(QtOpenGL.QGLWidget):
    """
    The GLWidget class for all GX applications.

    @param parent The parent of this widget
    """
    # Most mouse types work in steps of 15 degrees, in which case the delta value
    # is a multiple of 120; i.e., 120 units * 1/8 = 15 degrees.
    WHEELFACTOR = 1 /  8 / 15

    #__camera_dolly__  = ":/icons/camera-dolly.png"
    #__camera_pan__    = ":/icons/camera-pan.png"
    #__camera_orbit__  = ":/icons/camera-orbit.png"
    #__camera_roll__   = ":/icons/camera-roll.png"

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self._model = None

        #cursor_pixmap = QtGui.QPixmap(self.__camera_dolly__)
        #cursor_pixmap.setMask(cursor_pixmap.mask())
        #self._cursor_dolly = QtGui.QCursor(cursor_pixmap.scaledToHeight(32))

        #cursor_pixmap = QtGui.QPixmap(self.__camera_pan__)
        #cursor_pixmap.setMask(cursor_pixmap.mask())
        #self._cursor_pan = QtGui.QCursor(cursor_pixmap.scaledToHeight(32))

        #cursor_pixmap = QtGui.QPixmap(self.__camera_orbit__)
        #cursor_pixmap.setMask(cursor_pixmap.mask())
        #self._cursor_orbit = QtGui.QCursor(cursor_pixmap.scaledToHeight(32))

        #cursor_pixmap = QtGui.QPixmap(self.__camera_roll__)
        #cursor_pixmap.setMask(cursor_pixmap.mask())
        #self._cursor_roll = QtGui.QCursor(cursor_pixmap.scaledToHeight(32))

    def _modelDataChanged(self, topLeft, bottomRight):
        self.update()

    def setModel(self, model):
        if self._model:
            self._model.dataChanged.disconnect(self._modelDataChanged)
        self._model = model
        self._model.dataChanged.connect(self._modelDataChanged)

        self.initializeGL()
        self.resizeGL(self.width(), self.height())

    def enterEvent(self, event):
        """
        Override the QtGui.QWidget the enterEvent.
        """
        self.setFocus()
        self.grabKeyboard()

    def leaveEvent(self, event):
        """
        Override the QtGui.QWidget the leaveEvent.
        """
        self.parent().setFocus()
        self.releaseKeyboard()

    def closeEvent(self, event):
        """
        Override the QtGui.QWidget closeEvent. If we are allowed to exit, exit.  Otherwise hide the window.

        @param event A QCloseEvent created when Qt receives a window close request for a top-level widget from the window system.
        """
        self._model = None
        super(GLWidget, self).closeEvent(event)

    def keyPressEvent (self, event):
        """
        Overriden event handler to receive key press events for the widget.

        @param event A QKeyEvent reflecting the key press information.
        """
        super(GLWidget, self).keyPressEvent(event)

    def cursor(self):
        """
        Overriden method to return the mouse cursor for this widget.

        @returns An instance of a PySide.QtGui.QCursor.
        """
        #return super(GLWidget, self).cursor(event)
        return PySide.QtGui.QCursor(QtCore.Qt.CrossCursor)

    def validateCamera(self, message):
        """
        Validate the model's active camera.
        """
        valid = hasattr(self._model, 'activeCamera') and self._model.activeCamera
        if not valid:
            from ui.messagebox import MessageBox
            MessageBox.critical(self, '{0} failed.'.format(message), 'The scene does not have an active camera.')
        return valid

    def wheelEvent(self, event):
        """
        Overriden event handler to receive wheel events for the widget.

        @param event A QWheelEvent reflecting the wheel event information.
        """
        if self.validateCamera('Camera dolly operation.'):
            # Most mouse types work in steps of 15 degrees, in which case the delta value
            # is a multiple of 120; i.e., 120 units * 1/8 = 15 degrees.
            delta = event.delta() * GLWidget.WHEELFACTOR
            self._model.activeCamera.dolly( - event.delta()  )
            self.updateGL()

    def mousePressEvent(self, event):
        """
        Overriden event handler to receive mouse press events for the widget.

        @param event A QMouseEvent reflecting the mouse press events.
        """
        self._mousex = event.x()
        self._mousey = event.y()

        #if not (event.buttons() & QtCore.Qt.NoButton):
        #    if event.modifiers() & QtCore.Qt.Modifier.ALT:
        #        if event.modifiers() & QtCore.Qt.Modifier.SHIFT:
        #            pass
        #        if event.buttons() & QtCore.Qt.LeftButton:
        #            self.setCursor(self._cursor_orbit)
        #        elif event.buttons() & QtCore.Qt.RightButton:
        #            self.setCursor(self._cursor_dolly)
        #        elif event.buttons() & QtCore.Qt.MidButton:
        #            self.setCursor(self._cursor_pan)
        #    if event.modifiers() & QtCore.Qt.Modifier.CTRL:
        #        if event.modifiers() & QtCore.Qt.Modifier.SHIFT:
        #            pass
        #        if event.buttons() & QtCore.Qt.LeftButton:
        #            self.setCursor(self._cursor_roll)
        #        if event.buttons() & QtCore.Qt.RightButton:
        #            self.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))

    def mouseReleaseEvent(self, event):
        """
        Overriden event handler to receive mouse press events for the widget.

        @param event A QMouseEvent reflecting the mouse press events.
        """
        self.unsetCursor()

    def mouseMoveEvent(self, event):
        """
        Overriden event handler to receive mouse move events for the widget.

        @param event A QMouseEvent reflecting the mouse move events.
        """
        if not (event.buttons() & QtCore.Qt.NoButton):
            # User is dragging a mouse click
            delta_x = event.x() - self._mousex
            delta_y = event.y() - self._mousey

            if delta_x == 0:
                pass
            if delta_y == 0:
                pass
            # Camera Opeeration

            if event.modifiers() & QtCore.Qt.Modifier.ALT:
                if event.modifiers() & QtCore.Qt.Modifier.SHIFT:
                    if not self._mouselock:
                        if abs(delta_y) > abs(delta_x):
                            self._mouselock = lambda x, y: (0,y)
                        elif abs(delta_x) > abs(delta_y):
                            self._mouselock = lambda x, y: (x,0)
                    if self._mouselock:
                        delta_x, delta_y = self._mouselock(delta_x, delta_y)
                else:
                    self._mouselock = None

                #QtGui.QToolTip.showText(event.globalPos(), "{0}, {1}".format(event.x(), event.y()), self, self.rect())

                if event.buttons() & QtCore.Qt.LeftButton:
                    if self.validateCamera('Camera tumble operation'):
                        self._model.activeCamera.tumble( delta_x , delta_y )
                elif event.buttons() & QtCore.Qt.RightButton:
                    if self.validateCamera('Camera dolly operation'):
                        self._model.activeCamera.dolly( - delta_y )
                elif event.buttons() & QtCore.Qt.MidButton:
                    if self.validateCamera('Camera track operation'):
                        # Note:  OpenGL's origin is bottom left, PySide origin is top left.
                        #        Flip the 'Y' for accurate tracking
                        self._model.activeCamera.track( delta_x, -delta_y )
            if event.modifiers() & QtCore.Qt.Modifier.CTRL:
                if event.modifiers() & QtCore.Qt.Modifier.SHIFT:
                    delta_y *= 10
                    delta_x *= 10
                if event.buttons() & QtCore.Qt.LeftButton:
                    if self.validateCamera('Camera roll operation'):
                        self._model.activeCamera.roll( - delta_x )
                if event.buttons() & QtCore.Qt.RightButton:
                    if self.validateCamera('Camera zoom operation'):
                        self._model.activeCamera.zoom( - delta_y )
            self.updateGL()
        self._mousex = event.x()
        self._mousey = event.y()

    def minimumSizeHint(self):
        """
        Overriden method of QGLWidget to return the recommeded minimum size during layout.
        """
        return QtCore.QSize(10, 10)

    def sizeHint(self):
        """
        Overriden method of QGLWidget to return the preferred size during layout.
        """
        return self.size()

    def initializeGL(self):
        """
        Overriden method of QGLWidget to handle once before the first call to PySide.QtOpenGL.QGLWidget.paintGL() or PySide.QtOpenGL.QGLWidget.resizeGL(), and then once whenever the widget has been assigned a new PySide.QtOpenGL.QGLContext.
        """
        if self._model:
            self._model.initializeGL()

    def paintGL(self):
        """
        Overriden method of QGLWidget handle whenever the widget needs to be painted.
        """
        if self._model:
            self._model.paintGL()

    def resizeGL(self, width, height):
        """
        Overriden method of QGLWidget handle whenever the widget has been resized.

        @param width The new width
        @param height the new height
        """
        if self._model:
            self._model.resizeGL(width, height)
