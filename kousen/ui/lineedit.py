from PySide import QtGui, QtCore

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

    filter = FilterLineEdit(None)
    filter.show()

    app.exec_()