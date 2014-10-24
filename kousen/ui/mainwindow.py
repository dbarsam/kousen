import sys
import os
from PySide import QtGui, QtCore
from kousen.math import Point3D
from kousen.core.propertymodel import PropertyItem, PropertyModel
from kousen.core.proxymodel import ColumnFilterProxyModel, UndoRedoProxyModel, TreeColumnFilterProxyModel
from kousen.scenegraph import SceneGraphItem
from kousen.gl.glscene import GLSceneNode, GLSceneModel
from kousen.gl.glcamera import *
from kousen.gl.glhud import *
from kousen.gl.glprimitive import *
from kousen.gl.glutil import GLScope, GLVariableScope, GLAttribScope, GLClientAttribScope, GLMatrixScope
from ui.itemdialog import ItemCreationDialog
from ui.uiloader import UiLoader

__form_class__, __base_class__ = UiLoader.loadUiType(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mainwindow.ui'))

class MainWindow(__form_class__, __base_class__):
    """
    The UI Main Window class handling all of the core UI logic.
    """
    __ui_file__ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mainwindow.ui')

    def __init__(self, parent=None):
        """
        Constructor.
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, widget):
        super(MainWindow, self).setupUi(widget)

        # Scene Graph Explorer
        self.sceneExplorer.reloadable = False
        self.sceneExplorer.immediate = True
        self.sceneExplorer.label = None
        self.sceneExplorer.view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.sceneExplorer.view.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.sceneExplorer.view.customContextMenuRequested.connect(self._sceneExplorerContextMenuRequested)
        self.sceneExplorer.view.currentSelectionChanged.connect(self._sceneExplorerSelectionChanged)

        # Property Editor
        self.propertyEditor.reloadable = False
        self.propertyEditor.immediate = True
        self.propertyEditor.label = None
        self.propertyEditor.view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.propertyEditor.view.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.propertyEditor.view.customContextMenuRequested.connect(self._propertyEditorContextMenuRequested)
        self.propertyEditor.view.currentSelectionChanged.connect(self._propertyEditorSelectionChanged)
        self.propertyEditor.view.setAlternatingRowColors(True)
        self.propertyEditor.push(PropertyModel(PropertyItem.Fields.headerdata(), self)) 
        self.propertyEditor.push(TreeColumnFilterProxyModel())

        # Actions
        self.actionNewScene.triggered.connect(self._sceneNew)
        self.actionInsertNode.triggered.connect(self._nodeInsert)
        self.actionRemoveNode.triggered.connect(self._nodeRemove)
        self.actionAquirePrimaryCamera.triggered.connect(self._cameraActivate)
        self.actionReleasePrimaryCamera.triggered.connect(self._cameraRelease)
        self.dockSceneExplorer.toggleViewAction().toggled.connect(self.actionViewSceneExplorer.setChecked)
        self.dockPropertyEditor.toggleViewAction().toggled.connect(self.actionViewPropertyEditor.setChecked)

    def _testScene(self):
        self.actionNewScene.trigger()
        self._nodeInsert([ColorCubeObject()])

    def _sceneNew(self):
        # Scene Graph Model
        self._sceneGraph = GLSceneModel(SceneGraphItem.Fields.headerdata(), self)

        # Scene Graph Explorer's Scene Graph Model Views
        self.sceneExplorer.clear()
        self.sceneExplorer.push(self._sceneGraph) 
        self.sceneExplorer.push(TreeColumnFilterProxyModel())

        # OpenGL Scene Graph Model View
        self.glwidget.setModel(self._sceneGraph)

        camera = GLCameraNode()
        self._nodeInsert([camera, GLCameraHUDNode(camera), GridObject(16, 1)], False)
        self._cameraActivate(camera)

    def _nodeInsert(self, nodes=[], autoselect=True):
        if not nodes:
            dlg = ItemCreationDialog(self)
            nodetypes = dlg.selection() if dlg.show_() else []
            nodes = [node() for node in nodetypes]

        parentIndexes = self.sceneExplorer.selectedIndexes or [QtCore.QModelIndex()]
        indexes = []
        for node in nodes:
            for parentIndex in parentIndexes:
                indexes.append( self.sceneExplorer.source.appendItem(node, parentIndex) )

        if indexes:
            self.glwidget.update()
            if autoselect:
                self.sceneExplorer.selectedIndexes = indexes

    def _nodeRemove(self, nodes=[]):
        if not nodes:
            nodes = self.sceneExplorer.selectedItems
        for node in nodes:
            self.sceneExplorer.source.removeItem(node)
        if nodes:
            self.glwidget.update()

    def _cameraActivate(self, node=None):
        if not node:
            node = next( (n for n in self.sceneExplorer.selectedItems if type(n) is GLCameraNode), None)
        if node:
            self.sceneExplorer.source.activeCamera = node
            #for hud in [n for n in nodes if type(n) is CameraHUDNode]:
            #    hud.camera = node

    def _cameraRelease(self):
        self.sceneExplorer.source.activeCamera = None

    def _sceneExplorerContextMenuRequested(self, pos):
        """
        Handles the Custom Context Menu Requested event from the Scene Explorer.

        @param pos   The global position of the request.
        """
        menu = QtGui.QMenu()
        
        nodes = self.sceneExplorer.selectedItems
        cameras = [n for n in nodes if type(n) is GLCameraNode]
        if any(c == self.sceneExplorer.source.activeCamera for c in cameras):
            menu.addAction(self.actionReleasePrimaryCamera)
        if any(c != self.sceneExplorer.source.activeCamera for c in cameras):
            menu.addAction(self.actionAquirePrimaryCamera)
        if cameras:
            menu.addSeparator()
        menu.addActions([self.actionInsertNode, self.actionRemoveNode])
        menu.exec_(QtGui.QCursor.pos())

    def _sceneExplorerSelectionChanged(self, selected, deselected):
        """
        Handles the Selection Changed event from the Scene Explorer.

        @param selected   The new selection (which may be empty)
        @param deselected The previous selection (which may be empty)
        """
        sourceSelected = self.sceneExplorer.mapSelectionToSourceItem(selected)
        self.propertyEditor.source.insertProperties(sourceSelected)
        sourceDeselected = self.sceneExplorer.mapSelectionToSourceItem(deselected)        
        self.propertyEditor.source.removeProperties(sourceDeselected)

    def _propertyEditorContextMenuRequested(self, pos):
        """
        Handles the Custome Context Menu Requested event from the Property Editor.

        @param pos   The global position of the request.
        """
        menu = QtGui.QMenu()       
        menu.exec_(QtGui.QCursor.pos())

    def _propertyEditorSelectionChanged(self, selected, deselected):
        """
        Handles the Selection Changed event from the Property Editor.

        @param selected   The new selection (which may be empty)
        @param deselected The previous selection (which may be empty)
        """
        sourceSelected = self.sceneExplorer.mapSelectionToSource(selected)
        if sourceSelected:
            pass

