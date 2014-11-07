# -*- coding: utf-8 -*-
import os
from PySide import QtGui, QtCore
from PySide import QtGui, QtCore
from kousen.ui.uiloader import UiLoader

__form_class__, __base_class__ = UiLoader.loadUiType(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'messagebox.ui'))

class MessageBox(__form_class__, __base_class__):
    def __init__(self, parent, message, details=None, title="Kousen", pixmap=None, buttons=[]):
        """
        Base Constructor of the MessageBox.

        @param parent    The MessageBox's parent window
        @param message   The MessageBox's main message
        @param details   The raw text to display in the additional details message.  A value of None will remove the section.
        @param title     The MessageBox's window title
        @param pixmap    The MessageBox's icon
        @param buttons   The MessageBox's list of available buttons
        """
        super(MessageBox, self).__init__(parent, QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.WindowTitleHint)

        self.setupUi(self)

        self.setVisible(False)
        self.setWindowTitle(title)

        self._setIcon(pixmap)
        self._setButtons(buttons)
        self._setDetails(details)
        self._setMessage(message)
        self._setMinSize()

    def setupUi(self, widget):
        super(MessageBox, self).setupUi(widget)

        self.buttonDetails.toggled.connect(self._toggleDetails)

    def _setIcon(self, pixmap):
        """
        Define the Dialog characteristics based on the input type.

        @param pixmap  The MessageBox's icon
        """
        icon = QtGui.QIcon()
        icon.addPixmap( self.style().standardPixmap( pixmap ) )
        self.setWindowIcon(icon)
        self.labelIcon.setPixmap(self.style().standardPixmap( pixmap ))

    def _setButtons(self, buttons):
        """
        Define the Dialog characteristics based on the input type.

        @param buttons The MessageBox's list of available buttons
        """
        for b in buttons:
            self.btnboxButtons.addButton(b)
            self.btnboxButtons.button(b).clicked.connect(lambda x=b: self._buttonclicked(x))

    def _setMessage(self, message):
        """
        Internal method to manage the message of the MessageBox

        @param message   The MessageBox's main message
        """
        self.lblMessage.setText(message)

    def _setDetails(self, text):
        """
        Internal method to manage the Details Window of the MessageBox

        @param text  The raw details text.
        """
        enable = bool(text)

        self.texteditDetails.insertPlainText(text)
        self.texteditDetails.moveCursor(QtGui.QTextCursor.Start)

        self.buttonDetails.setVisible(enable)
        self.frameDetails.setVisible(enable)

        self.buttonDetails.setChecked(False)
        self._toggleDetails(False)

    def _setMinSize(self):
        """
        Internal method to manage the size of the MessageBox.
        """
        self.setMinimumHeight(0)
        self.resize(self.minimumWidth(), self.minimumHeight())

    def _toggleDetails(self, state):
        """
        Internal method to toggle the Details panel.

        @param state: True if visible; False otherwise
        """
        self.frameDetails.setVisible(state)

        pixmap = QtGui.QPixmap( ":/icons/chevron-down.png" if state else ":/icons/chevron-right.png" )
        icon = QtGui.QIcon()
        icon.addPixmap( pixmap )

        self.buttonDetails.setIcon(icon)
        self.buttonDetails.setText("Details...")

        self._setMinSize()

    def _buttonclicked(self, button):
        """
        Internal event handler for the button clicked event.

        @param button    The MessageBox's button that has been clicked
        """
        if button == QtGui.QDialogButtonBox.StandardButton.Ok:
            self.accept()
        elif button == QtGui.QDialogButtonBox.StandardButton.Yes:
            self.accept()
        elif button == QtGui.QDialogButtonBox.StandardButton.No:
            self.reject()

    def show_(self):
        """
        Method to display the MessageBox using the correct internal PySide details
        """
        return self.exec_()

    @staticmethod
    def warning(parent, message, details=None):
        """
        Static function to launch a MessageBox in the Warning style preset

        @param parent    The MessageBox's parent window
        @param message   The MessageBox's main message
        @param details   A raw text block to details in the 'details' section.  A value of None will remove the section.
        """
        return MessageBox(parent, message, details, "Kousen Warning", QtGui.QStyle.SP_MessageBoxWarning, [QtGui.QDialogButtonBox.Ok]).show_()

    @staticmethod
    def question(parent, message, details=None):
        """
        Static function to launch a MessageBox in the Question style preset

        @param parent    The MessageBox's parent window
        @param message   The MessageBox's main message
        @param details   A raw text block to details in the 'details' section.  A value of None will remove the section.
        """
        return MessageBox(parent, message, details, "Kousen Question", QtGui.QStyle.SP_MessageBoxQuestion, [QtGui.QDialogButtonBox.Yes, QtGui.QDialogButtonBox.No]).show_()

    @staticmethod
    def critical(parent, message, details=None):
        """
        Static function to launch a MessageBox in the Critical style preset

        @param parent    The MessageBox's parent window
        @param message   The MessageBox's main message
        @param details   A raw text block to details in the 'details' section.  A value of None will remove the section.

        """
        return MessageBox(parent, message, details,"Kousen Critical", QtGui.QStyle.SP_MessageBoxCritical, [QtGui.QDialogButtonBox.Ok]).show_()

    @staticmethod
    def information(parent, message, details=None):
        """
        Static function to launch a MessageBox in the Information style preset

        @param parent    The MessageBox's parent window
        @param message   The MessageBox's main message
        @param details   A raw text block to details in the 'details' section.  A value of None will remove the section.
        """
        return MessageBox(parent, message, details, "Kousen Information", QtGui.QStyle.SP_MessageBoxInformation, [QtGui.QDialogButtonBox.Ok]).show_()

    @staticmethod
    def exception(parent, message, exception=None, details=None):
        """
        Static function to launch a MessageBox in the Critical style preset

        @param parent    The MessageBox's parent window
        @param message   The MessageBox's main message
        @param exception An instance of a Python Exception class.
        @param details   A raw text block to details in the 'details' section.  It will be appended to the exception information as an 'Additional Details' section; a value of None will remove the 'Additional Details' section.
        """
        from core.exception import ExceptionMessage
        return MessageBox(parent, message, "{0}\n\n{1}".format(ExceptionMessage(exception), "Additional Details:\n{0}".format(details) if details else ""), "Kousen Critical Exception", QtGui.QStyle.SP_MessageBoxCritical, [QtGui.QDialogButtonBox.Ok]).show_()

if __name__ == "__main__":
    app = QtGui.QApplication.instance()
    if not app: app = QtGui.QApplication([])

    for x in [MessageBox.critical, MessageBox.question, MessageBox.warning, MessageBox.information]:
        x(None, "Test Message", "Additional Details")
    try:
        raise Exception("Test Exception!")
    except Exception as e:
        MessageBox.exception(None, "Test Exception", e, "Extra information")
    app.exec_()
