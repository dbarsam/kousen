from PySide import QtGui, QtCore
from kousen.ui.lineedit import ColorLineEdit

class ColorEditor(ColorLineEdit):
    """
    The ColorEditor class provides a modified ColorLineEdit with a QProperty as required by QItemEditorFactory.
    """    
    color = QtCore.Property('QColor', ColorLineEdit.getColor, ColorLineEdit.setColor, user=True)

    def __init__(self, parent=None):
        """
        Constructor
        """
        super(ColorEditor, self).__init__(parent)   

class ColorEditorCreator(QtGui.QItemEditorCreatorBase):
    """
    The ColorEditorCreator implements a QItemEditorCreatorBase that creates a ColorLineEdit.
    """
    def __init__(self):
        """
        Constructor
        """
        super(ColorEditorCreator, self).__init__()

    def createWidget(self, parent):
        """
        Overrides the QtGui.QItemEditorCreatorBase createWidget method to create the ColorLineEditor..

        @param parent The object to uses as the parent of the ColorLineEditor.
        @return An instance of the ColorEditor
        """
        editor = ColorEditor(parent)
        editor.setFrame(False)
        return editor

class ItemEditorFactory(QtGui.QItemEditorFactory):
    """
    The ItemEditorFactory implements a ItemEditorFactory registered with all editors created in the kousen.ui.editorfactory module.    
    """
    # Define a table of types and respective editor to register with this instance
    typeEditors = { QtGui.QColor : ColorEditorCreator }

    def __init__(self):
        """
        Constructor
        """
        super(ItemEditorFactory, self).__init__()
        for k,v in ItemEditorFactory.typeEditors.items():
            self.registerEditor(k, v())

class ItemEditorFactoryDelegate(QtGui.QStyledItemDelegate):
    """
    The ItemEditorFactoryDelegate implements a QStyledItemDelegate registered with the kousen.ui.editorfactory module's ItemEditorFactory.
    """
    def __init__(self, parent=None):
        super(ItemEditorFactoryDelegate, self).__init__(parent)
        self.setItemEditorFactory(ItemEditorFactory())

    def updateEditorGeometry(self, editor, option, index):
        """
        Overrides the QtGui.QStyledItemDelegate updateEditorGeometry method to update the editor for the item specified by index according to the style option given.

        @param editor An instance of the current editor.
        @param option An instance of QStyleOptionViewItem.
        @param index  An QModelIndex representing the current item.
        """
        if isinstance(editor, ColorLineEdit):
            editor.setGeometry(option.rect)
        else:
            super(ItemEditorFactoryDelegate, self).updateEditorGeometry(editor, option, index)
