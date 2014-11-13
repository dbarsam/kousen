# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
from kousen.ui.lineedit import ColorLineEdit

class ColorEditor(ColorLineEdit):
    """
    The ColorEditor class provides a modified ColorLineEdit with a QtCore.Property as required by QItemEditorFactory.
    """
    qproperty = QtCore.Property('QColor', ColorLineEdit.getColor, ColorLineEdit.setColor, user=True)

    def __init__(self, parent=None):
        """
        Constructor

        @param parent The parent widget of this widget.
        """
        super(ColorEditor, self).__init__(parent)
        self.setFrame(False)

class ItemEditorCreator(QtGui.QItemEditorCreatorBase):
    """
    The ItemEditorCreator implements a QStandardItemEditorCreator that creates an editor widget from a provided editor widget type.
    """
    def __init__(self, widgetType):
        """
        Constructor
        @param widgetType The type to instantiate in the createWidet method.
        """
        super(ItemEditorCreator, self).__init__()
        self._widgetType = widgetType

    def createWidget(self, parent):
        """
        Overrides the QtGui.QItemEditorCreatorBase createWidget method to create the editor widget instance.

        @param parent The object to use as the parent of the editor widget.
        @return An instance of the editor widget with the given parent.
        """
        return self._widgetType(parent)

    def valuePropertyName(self):
        """
        Overrides the QtGui.QItemEditorCreatorBase valuePropertyName method to return the Editor's QProperty.
        
        @return The name of the property used to get and set values in the creator's editor widgets.
        """
        return self._widgetType.staticMetaObject.userProperty().name()

class ItemEditorFactory(QtGui.QItemEditorFactory):
    """
    The ItemEditorFactory implements a ItemEditorFactory registered with all editors created in the kousen.ui.editorfactory module.
    """
    # Define a table of types and respective editor to register with this instance
    typeEditors = { QtGui.QColor : ColorEditor }

    def __init__(self):
        """
        Constructor
        """
        super(ItemEditorFactory, self).__init__()
        # Register the ItemEditorCreator or the widget with an ItemEditorCreator
        for k,v in ItemEditorFactory.typeEditors.items():
            if issubclass(v, QtGui.QItemEditorCreatorBase):
                self.registerEditor(k, v())
            else:
                self.registerEditor(k, ItemEditorCreator(v))

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
