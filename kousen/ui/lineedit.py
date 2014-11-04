from PySide import QtGui, QtCore

class ColorLineEdit(QtGui.QLineEdit):
    """
    The ColorLineEdit class provides a modified QLineEdit with a Color decoration and a 'browse' button to launch a QtGui.QColorDialog.
    """
    colorChanged = QtCore.Signal(QtGui.QColor)    
    colorRegex   = QtCore.QRegExp('^#[A-Fa-f0-9]{6}')

    def __init__(self, parent=None):
        """
        Constructor
        """
        super(ColorLineEdit, self).__init__(parent)

        self._lbutton = QtGui.QToolButton(self)        
        self._lbutton.setCursor(QtCore.Qt.ArrowCursor)
        self._lbutton.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Maximum)
        self._lbutton.setStyleSheet("QToolButton { background-color: transparent; border: none; padding: 0px;}")

        self._rbutton = QtGui.QToolButton(self)
        self._rbutton.setText('...')
        self._rbutton.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Maximum)
        self._rbutton.setCursor(QtCore.Qt.ArrowCursor)
        self._rbutton.clicked.connect(self.showDialog)

        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        rbuttonSize = self._rbutton.sizeHint()
        lbuttonSize = self._lbutton.sizeHint()
        self.setStyleSheet('QLineEdit {padding-left: %dpx; padding-right: %dpx; }' % (lbuttonSize.width() + frameWidth + 1, rbuttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), lbuttonSize.width() + rbuttonSize.width() + frameWidth*2 + 2), self.minimumSizeHint().height())

        self.setValidator(QtGui.QRegExpValidator(ColorLineEdit.colorRegex, self))
        
        self.editingFinished.connect(lambda: self.setColor(QtGui.QColor(self.text())))

        self.setColor(QtGui.QColor(0,0,0))

    def resizeEvent(self, event):
        """
        Overrides the QtGui.QWidget resizeEvent method for custom resize handling.

        @param event A QResizeEvent containing the resize parameters.
        """
        super(ColorLineEdit, self).resizeEvent(event)
        
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        
        rbuttonSize = QtCore.QSize(self._rbutton.sizeHint().width(), (self.height() - frameWidth * 2))        
        self._rbutton.setFixedSize(rbuttonSize)
        self._rbutton.move(self.rect().right() - frameWidth - rbuttonSize.width(), (self.rect().bottom() + 1 - rbuttonSize.height())/2)

        lbuttonSize = QtCore.QSize(self._lbutton.sizeHint().width(), (self.height() - frameWidth * 2))                
        self._lbutton.setFixedSize(lbuttonSize)
        self._lbutton.move(self.rect().left() + frameWidth + 1, self.rect().top() + frameWidth)
        
    def showDialog(self):
        """
        Launches the Color Dialog and stores the resulting color, if valid.
        """
        color = QtGui.QColorDialog.getColor(self.getColor(), self)
        if color.isValid():
            self.setColor(color)

    def getColor(self):
        """
        Gets the current value color.

        @return A valid QtGui.QColor instance.
        """
        return self._color

    def setColor(self, color):
        """
        Sets the current value color.

        @param color A valid QtGui.QColor instance.
        """
        self._color = color
        
        pixmap = QtGui.QPixmap(5,5)
        pixmap.fill(color)
        self._lbutton.setIcon(QtGui.QIcon(pixmap.scaled(self._lbutton.sizeHint(), QtCore.Qt.KeepAspectRatio)))
        
        self.setText(color.name())

        self.colorChanged.emit(self._color)

class FilterLineEdit(QtGui.QLineEdit):
    """
    The FilterLineEdit class provides a modified QLineEdit with a filter state icon.
    """
    activated = QtCore.Signal(bool)

    def __init__(self, parent=None):
        """
        Constructor.
        """
        super(FilterLineEdit, self).__init__(parent)

        self._searchPixmap = QtGui.QPixmap(":/icons/search.png")
        self._cancelPixmap = QtGui.QPixmap(":/icons/cancel.png")

        self._button = QtGui.QToolButton(self)
        self._button.setIcon(QtGui.QIcon(self._searchPixmap))
        self._button.setCursor(QtCore.Qt.ArrowCursor)
        self._button.setStyleSheet("QToolButton { background-color: transparent; border: none; padding: 0px; }")
        self._button.show()
        self._button.setEnabled(False)

        self._button.clicked.connect(self.clear)
        self.textChanged.connect(self.updateState)

        self.setProperty("isActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.setStyleSheet("padding-right: {0}px".format(self._button.sizeHint().width() + frameWidth + 1))

        minSize = self.minimumSizeHint()
        self.setMinimumSize(max(minSize.width(), self._button.sizeHint().width() + frameWidth * 2 + 2),
                            max(minSize.height(), self._button.sizeHint().height() + frameWidth * 2 + 2))

    def active(self):
        return self.property("isActive")

    def resizeEvent(self, event):
        super(FilterLineEdit, self).resizeEvent(event)
        buttonSize = self._button.sizeHint()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self._button.move(self.rect().right() - frameWidth - buttonSize.width(), (self.rect().bottom() + 1 - buttonSize.height())/2)

    def updateState(self, text):
        active = self.property("isActive")
        if active != bool(text):
            active = bool(text)
            self.setProperty("isActive", active)
            if active:
                self._button.setIcon(QtGui.QIcon(self._cancelPixmap))
            else:
                self._button.setIcon(QtGui.QIcon(self._searchPixmap))
            self.activated.emit(active)
            self._button.setEnabled(active)
            self.setProperty("isActive", active)
            self.style().unpolish(self)        
            self.style().polish(self)
            self.update()
        

if __name__ == "__main__":
    import sys
    import os
    
    packagepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if not packagepath in sys.path:
        sys.path.append(packagepath)

    import kousen.resources_rc

    app = QtGui.QApplication.instance()
    if not app: app = QtGui.QApplication([])

    filterline = FilterLineEdit(None)
    filterline.show()

    colorline = ColorLineEdit(None)
    colorline.show()

    app.exec_()