import sys
import os
from PySide import QtGui, QtCore
from kousen.math import Point3D
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

        # Scene Graph TreeWidget
        self.treewidget.reloadable = False
        self.treewidget.immediate = True
        self.treewidget.label = None
        self.treewidget.view.customContextMenuRequested.connect(self._treeViewContextMenuRequested)
        self.treewidget.view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treewidget.view.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        self.splitter.setCollapsible(0, True)
        self.splitter.setCollapsible(1, True)
        self.splitter.setSizes([self.splitter.width() * 0.25, self.splitter.width() *0.75])

        # Menu
        self.menuFile.addAction(self.actionNewScene)

        # Actions
        self.actionNewScene.triggered.connect(self._sceneNew)
        self.actionInsertNode.triggered.connect(self._nodeInsert)
        self.actionRemoveNode.triggered.connect(self._nodeRemove)
        self.actionAquirePrimaryCamera.triggered.connect(self._cameraActivate)
        self.actionReleasePrimaryCamera.triggered.connect(self._cameraRelease)
        self.actionExit.triggered.connect(self.close)

    def _testScene(self):
        self.actionNewScene.trigger()
        self._nodeInsert([TestPattern()])

    def _sceneNew(self):
        # Scene Graph Model
        self._sceneGraph = GLSceneModel(SceneGraphItem.Fields.headerdata(), self)

        # Tree View Scene Graph Model Views
        self.treewidget.clear()
        self.treewidget.label = "<NewScene>"
        self.treewidget.push(self._sceneGraph) 
        self.treewidget.push(TreeColumnFilterProxyModel())

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

        parentIndexes = self.treewidget.selectedIndexes or [QtCore.QModelIndex()]
        indexes = []
        for node in nodes:
            for parentIndex in parentIndexes:
                indexes.append( self.treewidget.source.appendItem(node, parentIndex) )

        if indexes:
            self.glwidget.update()
            if autoselect:
                self.treewidget.selectedIndexes = indexes

    def _nodeRemove(self, nodes=[]):
        if not nodes:
            nodes = self.treewidget.selectedItems
        for node in nodes:
            self.treewidget.source.removeItem(node)
        if nodes:
            self.glwidget.update()

    def _cameraActivate(self, node=None):
        if not node:
            node = next( (n for n in self.treewidget.selectedItems if type(n) is GLCameraNode), None)
        if node:
            self.treewidget.source.activeCamera = node
            #for hud in [n for n in nodes if type(n) is CameraHUDNode]:
            #    hud.camera = node

    def _cameraRelease(self):
        self.treewidget.source.activeCamera = None

    def _treeViewContextMenuRequested(self, pos):
        menu = QtGui.QMenu()
        
        nodes = self.treewidget.selectedItems
        cameras = [n for n in nodes if type(n) is GLCameraNode]
        if any(c == self.treewidget.source.activeCamera for c in cameras):
            menu.addAction(self.actionReleasePrimaryCamera)
        if any(c != self.treewidget.source.activeCamera for c in cameras):
            menu.addAction(self.actionAquirePrimaryCamera)
        if cameras:
            menu.addSeparator()
        menu.addActions([self.actionInsertNode, self.actionRemoveNode])
        menu.exec_(QtGui.QCursor.pos())

