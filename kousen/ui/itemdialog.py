import os
from PySide import QtGui, QtCore
from PySide import QtGui, QtCore
from PySide import QtCore, QtGui
from kousen.core.proxymodel import ColumnFilterProxyModel, TreeColumnFilterProxyModel, ColumnFilterDataProxyModel
from kousen.core.abstractmodel import AbstractDataItem, AbstractData, AbstractDataListModel
from kousen.scenegraph import SceneGraphItem
from kousen.scenegraph import SceneGraphType, SceneGraphTypeTreeModel
from kousen.ui.uiloader import UiLoader
from kousen.scenegraph import SceneGraphType, SceneGraphTypeTreeModel
from kousen.gl.glscene import *
from kousen.gl.glcamera import *
from kousen.gl.glhud import *
from kousen.gl.glprimitive import *
from kousen.gl.gltransform import *
from kousen.gl.glutil import GLScope, GLVariableScope, GLAttribScope, GLClientAttribScope, GLMatrixScope

__form_class__, __base_class__ = UiLoader.loadUiType(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'itemdialog.ui'))

class ItemDialog(__form_class__, __base_class__):
    def __init__(self, parent):
        """
        Base Constructor of the ItemDialog.

        @param parent    The ItemDialog's parent window
        """
        super(ItemDialog, self).__init__(parent, QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.WindowTitleHint)        
        self.setupUi(self)

    def setupUi(self, widget):
        super(ItemDialog, self).setupUi(widget)

    def show_(self):
        """
        Method to display the ItemDialog using the correct internal PySide details
        """
        return self.exec_()

class ItemCreationDialog(ItemDialog):
    def __init__(self, parent):
        """
        Base Constructor of the ItemDialog.
        @param parent    The ItemDialog's parent window
        """
        super(ItemCreationDialog, self).__init__(parent)

    def setupUi(self, widget):
        super(ItemDialog, self).setupUi(widget)
        self.treewidget.push(SceneGraphTypeTreeModel(SceneGraphType.Fields.headerdata(), self)) 
        self.treewidget.push(TreeColumnFilterProxyModel())
        self.treewidget.reload()
        self.treewidget.immediate = True
        self.treewidget.label = "Scene Graph Items"
        self.treewidget.view.doubleClicked.connect(self._doubleClicked)

    def _doubleClicked(self, index):
        item = self.treewidget.mapToSourceItem(index)
        if item.data(SceneGraphType.Fields.CLASS):
            self.accept()

    def selection(self):
        return [item[SceneGraphType.Fields.CLASS] for item in self.treewidget.selectedItems]

    def show_(self):
        """
        Method to display the ItemDialog using the correct internal PySide details
        """
        return self.exec_()

if __name__ == "__main__":
    app = QtGui.QApplication.instance()
    if not app: app = QtGui.QApplication([])

    dlg = ItemCreationDialog(None)

    if dlg.show_():
        items = dlg.selection()
    else:
        items = []
    app.exec_()
