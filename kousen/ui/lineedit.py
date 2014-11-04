from PySide import QtGui, QtCore

class LineFilter(QtGui.QLineEdit):
    """A QLineEdit derived class"""
    
    activated = QtCore.Signal(bool)

    def __init__(self, parent=None):
        """
        Constructor.
        """
        super(LineFilter, self).__init__(parent)

        self.__searchPixmap = QtGui.QPixmap(":/icons/search.png")
        self.__cancelPixmap = QtGui.QPixmap(":/icons/cancel.png")

        self.__button = QtGui.QToolButton(self)
        self.__button.setIcon(QtGui.QIcon(self.__searchPixmap))
        self.__button.setCursor(QtCore.Qt.ArrowCursor)
        self.__button.setStyleSheet("QToolButton { background-color: transparent; border: none; padding: 0px; }")
        self.__button.show()
        self.__button.setEnabled(False)

        self.__button.clicked.connect(self.clear)
        self.textChanged.connect(self.updateState)

        self.setProperty("isActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.setStyleSheet("padding-right: {0}px".format(self.__button.sizeHint().width() + frameWidth + 1))

        minSize = self.minimumSizeHint()
        self.setMinimumSize(max(minSize.width(), self.__button.sizeHint().width() + frameWidth * 2 + 2),
                            max(minSize.height(), self.__button.sizeHint().height() + frameWidth * 2 + 2))

    def active(self):
        return self.property("isActive")

    def resizeEvent(self, event):
        super(LineFilter, self).resizeEvent(event)
        buttonSize = self.__button.sizeHint()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.__button.move(self.rect().right() - frameWidth - buttonSize.width(), (self.rect().bottom() + 1 - buttonSize.height())/2)

    def updateState(self, text):
        active = self.property("isActive")
        if active != bool(text):
            active = bool(text)
            self.setProperty("isActive", active)
            if active:
                self.__button.setIcon(QtGui.QIcon(self.__cancelPixmap))
            else:
                self.__button.setIcon(QtGui.QIcon(self.__searchPixmap))
            self.activated.emit(active)
            self.__button.setEnabled(active)
            self.setProperty("isActive", active)
            self.style().unpolish(self)        
            self.style().polish(self)
            self.update()
        
