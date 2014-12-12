# -*- coding: utf-8 -*-
import sys
import os
from PySide import QtGui, QtCore
from kousen.math import Point3D
from kousen.core.propertymodel import PropertyItem, PropertyModel
from kousen.core.proxymodel import ColumnFilterProxyModel, TreeColumnFilterProxyModel
from kousen.gl.glscene import GLSceneNode, GLSceneModel
from kousen.gl.glcamera import *
from kousen.gl.glhud import *
from kousen.gl.glprimitive import *
from kousen.gl.glutil import GLScope, GLVariableScope, GLAttribScope, GLClientAttribScope, GLMatrixScope
from kousen.ui.itemdialog import ItemCreationDialog
from kousen.ui.uiloader import UiLoader
from kousen.ui.editorfactory import ItemEditorFactoryDelegate
from kousen.core.undomodel import UndoMacro

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
        self._sceneGraph = None
        self.setupUi(self)

    def setupUi(self, widget):
        """
        Initializes the local state of the UI class.

        @param widget The instance of the UI class.
        """
        super(MainWindow, self).setupUi(widget)

        # Undo View
        self._undoStack = QtGui.QUndoStack(self);
        self.commandHistory.setStack(self._undoStack)

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
        self.propertyEditor.view.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged)
        self.propertyEditor.view.setItemDelegateForColumn(PropertyItem.Fields.VALUE, ItemEditorFactoryDelegate(self.propertyEditor.view))
        self.propertyEditor.push(PropertyModel(PropertyItem.Fields.headerdata(), self))
        self.propertyEditor.model.setUndoModel(self._undoStack)
        self.propertyEditor.push(TreeColumnFilterProxyModel())

        # Actions
        self.actionNewScene.triggered.connect(self._sceneNew)
        self.actionInsertNode.triggered.connect(self._nodeInsert)
        self.actionRemoveNode.triggered.connect(self._nodeRemove)
        self.actionAquirePrimaryCamera.triggered.connect(self._cameraActivate)
        self.actionReleasePrimaryCamera.triggered.connect(self._cameraRelease)
        self.dockSceneExplorer.toggleViewAction().toggled.connect(self.actionViewSceneExplorer.setChecked)
        self.dockPropertyEditor.toggleViewAction().toggled.connect(self.actionViewPropertyEditor.setChecked)
        self.dockCommandHistory.toggleViewAction().toggled.connect(self.actionViewCommandHistory.setChecked)
        self.actionEditRedo.triggered.connect(self._redoAction)
        self.actionEditUndo.triggered.connect(self._undoAction)

        # Menus
        self.menuEdit.aboutToShow.connect(self._editAboutToShow)

    def _testScene(self):
        """
        Debug Function to quickly create a scene
        """
        self.actionNewScene.trigger()
        self._nodeInsert([ColorCubeObject()])

    def _editAboutToShow(self):
        """
        Handles the Edit Menu before it is shown to the user.
        """
        self.actionEditUndo.setEnabled(self._undoStack.canUndo())
        self.actionEditRedo.setEnabled(self._undoStack.canRedo())

    def _sceneDataChanged(self, topLeft, bottomRight):
        """
        Handles any change in scene data.
        """
        self.glwidget.update()

    def _sceneRowsInserted(self, parent, start, end):
        """
        Handles scene items being added to the scene model.
        """
        self.glwidget.update()

    def _sceneRowsRemoved(self, parent, start, end):
        """
        Handles scene items being remove from the scene model.
        """
        self.glwidget.update()

    def _undoAction(self):
        """
        Executes the undo operation from the current action in the undo model.
        """
        if self._undoStack.canUndo():
            self._undoStack.undo()

    def _redoAction(self):
        """
        Executes the redo operation from the current action in the undo model.
        """
        if self._undoStack.canRedo():
            self._undoStack.redo()

    def _sceneNew(self):
        """
        Creates a new scene.
        """
        # Undo Stack
        self._undoStack.clear()

        # Scene Graph Model
        if self._sceneGraph:
            self._sceneGraph.setUndoModel(None)
            self._sceneGraph.dataChanged.disconnect(self._sceneDataChanged)
            self._sceneGraph.rowsInserted.disconnect(self._sceneRowsInserted)
            self._sceneGraph.rowsRemoved.disconnect(self._sceneRowsRemoved)
        self._sceneGraph = GLSceneModel(self)
        self._sceneGraph.setUndoModel(self._undoStack)
        self._sceneGraph.dataChanged.connect(self._sceneDataChanged)
        self._sceneGraph.rowsInserted.connect(self._sceneRowsInserted)
        self._sceneGraph.rowsRemoved.connect(self._sceneRowsRemoved)

        # Scene Graph Explorer's Scene Graph Model Views
        self.sceneExplorer.clear()
        self.sceneExplorer.push(self._sceneGraph)
        self.sceneExplorer.push(TreeColumnFilterProxyModel())

        # OpenGL Scene Graph Model View
        self.glwidget.setModel(self._sceneGraph)

        with UndoMacro(self._undoStack, "New Scene"):
            camera = GLCameraNode()
            self._nodeInsert([camera, GLCameraHUDNode(camera), GridObject(16, 1)], False)
            self._cameraActivate(camera)

    def _nodeInsert(self, nodes=[], autoselect=True):
        """
        Insert nodes into the scene's scenegraph.

        @param nodes      A list of nodes to be inserted.
        @param autoselect Flag to denote that the new nodes will be selected immediately after insertion.
        """
        if not nodes:
            dlg = ItemCreationDialog(self)
            nodetypes = dlg.selection() if dlg.show_() else []
            nodes = [node() for node in nodetypes]

        parentIndexes = self.sceneExplorer.selectedIndexes or [QtCore.QModelIndex()]
        indexes = []
        for node in nodes:
            for parentIndex in parentIndexes:
                indexes.extend( self.sceneExplorer.source.appendItem(node, parentIndex) )

        if indexes:
            if autoselect:
                self.sceneExplorer.selectedIndexes = indexes

    def _nodeRemove(self, nodes=[]):
        """
        Remove nodes from the scene's scenegraph.

        @param nodes      A list of nodes to be removed.
        """
        if not nodes:
            nodes = self.sceneExplorer.selectedItems

        for node in nodes:
            self.sceneExplorer.source.removeItem(node)

    def _cameraActivate(self, node=None):
        """
        Activates a camera node in the scene graph, making it the scene graph's primary camera.

        @param node An instance of a camera node.
        """
        if not node:
            node = next( (n for n in self.sceneExplorer.selectedItems if type(n) is GLCameraNode), None)
        if node:
            self.sceneExplorer.source.activeCamera = node
            #for hud in [n for n in nodes if type(n) is CameraHUDNode]:
            #    hud.camera = node

    def _cameraRelease(self):
        """
        Deactivates the scene graph's currently activated camera.

        @note With no active camera the results may be unpredictable.
        """
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
        sourceDeselected = self.sceneExplorer.mapSelectionToSourceItem(deselected)
        self.propertyEditor.source.removeProperties(sourceDeselected)

        sourceSelected = self.sceneExplorer.mapSelectionToSourceItem(selected)
        self.propertyEditor.source.insertProperties(sourceSelected)

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
        sourceSelected = self.propertyEditor.mapSelectionToSource(selected)
        if sourceSelected:
            pass