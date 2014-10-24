import os
from PySide import QtGui, QtCore

from kousen.ui.uiloader import UiLoader
from kousen.ui.views import TreeView

__form_class__, __base_class__ = UiLoader.loadUiType(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'filteredview.ui'))

class FilteredView(__base_class__, __form_class__):
    """
    The FilteredView class provides associates a filter widget with a view widget.

    The Qt method of filtering uses proxy models inserted between the view and the source model
        view -> proxy n -> ... -> proxy 0 -> source
    While the model contains the original data, each proxy alters the index mapping and presents this mapping to the view. Qt manages this quite well, this relationship needs to be accounted for when querying the data or setting selection.
    """
    viewUpdating     = QtCore.Signal()
    viewUpdated      = QtCore.Signal()

    def __init__(self, view = None, parent=None):
        """
        Constructor
        @param view    The initial instance the QAbstractItemView view widget
        @param parent  The parent of this widget.
        """
        super(FilteredView, self).__init__(parent)
        self.setupUi(self)

        self._stack = []
        self.actionReload.triggered.connect(self._reload)
        self.view = view
        self.immediate = True

    def _reload(self):
        """
        Internal method to invoke the model's data generation method.
        """
        try:
            self.viewUpdating.emit()
            self.source.reload()
            self.viewUpdated.emit()
        except Exception as e:
            from ui.messagebox import MessageBox
            MessageBox.exception(self, "Model Data Generation Failed:  Internal Exception.", e)

    def _filter(self, text = None):
        """
        Internal method to apply the proxy's filter mechanism.
        """
        regexp = QtCore.QRegExp(text if text else self.filterString.text(), QtCore.Qt.CaseInsensitive)
        proxies = self.proxies
        if self.proxies:
            for p in reversed(proxies): 
                p.setFilterRegExp(regexp)
        self.view.viewport().update()

    def _updateLayout(self):
        """
        Updates the layout
        """
        if any([self.buttonReload.isVisible(), self.filterLabel.isVisible()]):
            self.filterLayout.setSpacing(4)
        else:
            self.filterLayout.setSpacing(0)

    def showEvent(self, event):
        """
        Override the Dialog showEvent for custom hiding handling.

        @param event A QShowEvent created when Qt receives a window show request for a top-level widget from the window system.

        @note Non-spontaneous show events (initialization) are sent to widgets immediately before they are shown. The spontaneous show events (minimize, restore, etc) of windows are delivered afterwards.
        """
        self._updateLayout()
        return super(FilteredView, self).showEvent(event)

    @property
    def view(self):
        """
        Convenience property to access the source view.

        @returns The current view if valid; None otherwise.
        """
        return self.viewWidget if isinstance(self.viewWidget, QtGui.QAbstractItemView) else None

    @view.setter
    def view(self, value):
        """
        Convenience property to access the source view.

        @param value The view value.
        """  
        self.setView(value)

    @property
    def source(self):
        """
        Convenience property to access the source model.

        @returns The current model if valid; None otherwise.
        """
        return self._stack[0] if self._stack and not isinstance(self._stack[0], QtGui.QAbstractProxyModel) else None

    @property
    def proxy(self):
        """
        Convenience property to access the top most proxy model.

        @returns The current model if valid; None otherwise.
        """
        return self._stack[-1] if self._stack and isinstance(self._stack[-1], QtGui.QAbstractProxyModel) else None

    @property
    def model(self):
        """
        Convenience property to access the top most model.

        @returns The current model if valid; None otherwise.
        """
        return self._stack[-1] if self._stack else None

    @property
    def proxies(self):
        """
        Convenience property to access the list of proxies.

        @returns The current model if valid; None otherwise.
        """
        return [p for p in self._stack if isinstance(p, QtGui.QAbstractProxyModel)]

    @property
    def label(self):
        """
        Gets the text used for the display label.

        @returns The current text used in the display label.
        """
        return self.filterLabel.text()

    @label.setter
    def label(self, text):
        """
        Sets the display label text.

        @param text The text value.
        """ 
        self.filterLabel.setVisible(bool(text))
        self.filterLabel.setText(text or "")
        self._updateLayout()

    @property
    def reloadable(self):
        """
        Gets the reloadable state.

        @param True if the model can clear regenerate its item; False otherwise.
        """  
        return self.buttonReload.isVisible()

    @reloadable.setter
    def reloadable(self, value):
        """
        Sets the reloadable state.

        @param value The new reloadable state value.
        """  
        self.buttonReload.setVisible(value)
        self._updateLayout()

    @property
    def immediate(self):
        """
        Gets the immediate filtering state.

        @param True if filtering will happen immediately; False if the filtering will occur after a loss of focus.
        """  
        return self._immediate

    @immediate.setter
    def immediate(self, value):
        """
        Sets  the immediate filtering state.

        @param value The new immediate state value.
        """  
        self._immediate = value
        # Was never connected; PyQt raises TypeError, PySide raises RuntimeError
        try:
            self.filterString.editingFinished.disconnect(self._filter)
        except (TypeError, RuntimeError):
            pass
        try:
            self.filterString.textChanged.disconnect(self._filter)
        except (TypeError, RuntimeError):
            pass

        if self._immediate:
            self.filterString.textChanged.connect(self._filter)
        else:
            self.filterString.editingFinished.connect(self._filter)

    @property
    def items(self):
        """
        Gets a list of model data items.

        @returns A list of model data items.
        """
        items = [self.model.item( self.model.index(r, 0) ) for r in range(self.model.rowCount())]

    @property
    def filteredItems(self):
        """
        Gets a list of model data items that are passing the filter.

        @returns A list of model data items.
        """
        indexes = [self.mapToSource( self.proxy.index(r, c) ) for r in xrange(self.proxy.rowCount()) for c in xrange(self.proxy.columnCount())]
        items   = [self.model.item( mi ) for mi in indexes]
        uitems  = set()
        return [i for i in items if i not in uitems and not uitems.add(i)]

    @property
    def selectedIndexes(self):
        """
        Gets a list of source data indexes currently selected in the view

        @returns A list of model data indexes.
        """ 
        selection = self.view.selectedIndexes()
        return [self.mapToSource(mi) for mi in selection]

    @selectedIndexes.setter
    def selectedIndexes(self, indexes=[]):
        """
        Sets a list of source data items as the current selection in the view.

        @params A list of model data items.
        """ 
        selection = QtGui.QItemSelection()        
        selection.append([QtGui.QItemSelectionRange(index) for index in indexes])
        selection = self.mapSelectionFromSource( selection )
        self.view.selectionModel().select(selection, QtGui.QItemSelectionModel.ClearAndSelect)

    @property
    def selectedItems(self):
        """
        Gets a list of source data items currently selected in the view

        @returns A list of model data items.
        """ 
        selection = self.selectedIndexes
        items     = [self.source.item( mi ) for mi in selection]
        uitems    = set()
        return [i for i in items if i not in uitems and not uitems.add(i)]

    @selectedItems.setter
    def selectedItems(self, items=[]):
        """
        Sets a list of source data items as the current selection in the view.

        @params A list of model data items.
        """ 
        selection = QtGui.QItemSelection()        
        selection.append([QtGui.QItemSelectionRange(self.model.itemIndex(item)) for item in items])
        selection = self.mapSelectionFromSource( selection )
        self.view.selectionModel().select(selection, QtGui.QItemSelectionModel.ClearAndSelect)

    def setView(self, view):
        """
        Sets the view.

        @param view An instance of an QAbstractItemView to be used as the view.
        """
        current = None

        if self.viewWidget:
            self.layout().removeWidget(self.viewWidget)
            self.viewWidget.setParent(None)
            if isinstance(self.viewWidget, QtGui.QAbstractItemView):
                current = self.viewWidget.model()
                self.viewWidget.setModel(None)
        
        if view:
            self.layout().addWidget(view)
            if isinstance(view, QtGui.QAbstractItemView):
                view.setModel(current)

        self.viewWidget = view

    def reload(self):
        """
        Reloads the source model data.
        """
        self._reload()

    def push(self, model):
        """
        Pushes a model onto the model stack.

        @param model An instance of an QAbstractItemModel to be represented by the view.
        """
        if self.view:
            # Remve the current model (if any)
            current = self.view.model()
            self.view.setModel(None)

            # If a proxy, insert the proxy between current and the view.
            if isinstance(model, QtGui.QAbstractProxyModel):
                if model.sourceModel():
                    print ("WARNING: Replacing {0} with {1} in {2}.".format(model.sourceModel(), current, model))
                model.setSourceModel(current)
            elif current:
                print ("WARNING: Replacing {0} with {1} in {2}.".format(current, model, self.view))

            # The model goes to the 'top' of the stack
            self.view.setModel(model)
        
        self._stack.append(model)

    def pop(self):
        """
        Pops a model from the model stack.

        @returns The pop'ed model.
        """
        if not self._stack:
            return None

        current = self._stack.pop()
        
        if self.view:
            # Remove the current model (if any)
            if current != self.view.model():
                print ("WARNING: View out of synch with Model stack.  Expected {0} found {1}.".format(current, self._view.model()))

            model = self._stack[-1] if self._stack else None
            self.view.setModel(model)

            # If a proxy, remove the proxy from between current and the view.
            if isinstance(current, QtGui.QAbstractProxyModel):
                current.setSourceModel(None)

        return current

    def clear(self):
        """
        Pops a model from the model stack.

        @returns The pop'ed model.
        """
        # Clear the Filter
        self.filterString.clear()

        # Clear the Proxy stack
        while self.pop():
            pass

    def mapToSource(self, proxyIndex):
        """
        Converts an proxy index to the corresponding source index.
        """
        sourceIndex = proxyIndex
        for model in reversed(self._stack):
            if isinstance(model, QtGui.QAbstractProxyModel):
                sourceIndex = model.mapToSource(sourceIndex)
        return sourceIndex

    def mapToSourceItem(self, proxyIndex):
        """
        Converts an proxy index to the corresponding source index.
        """
        sourceIndex = self.mapToSource(proxyIndex)
        return self.source.item(sourceIndex)

    def mapFromSource(self, sourceIndex):
        """
        Converts an source index to the corresponding proxy index.
        """
        proxyIndex = sourceIndex
        for model in self._stack:
            if isinstance(model, QtGui.QAbstractProxyModel):
                proxyIndex = model.mapFromSource(proxyIndex)
        return proxyIndex

    def mapSelectionToSource (self, proxySelection ):
        """
        Converts an proxy selection to the corresponding source selection.
        """
        sourceSelection = proxySelection
        for model in reversed(self._stack):
            if isinstance(model, QtGui.QAbstractProxyModel):
                sourceSelection = model.mapSelectionToSource(sourceSelection)
        return sourceSelection

    def mapSelectionToSourceItem(self, proxySelection):
        """
        Converts an proxy selection to the corresponding source sitem list.
        """
        sourceSelection = self.mapSelectionToSource(proxySelection)
        return [self.source.item(i) for i in sourceSelection.indexes()]

    def mapSelectionFromSource ( self, sourceSelection ):
        """
        Converts an model selection to the corresponding proxy selection.
        """
        proxySelection = sourceSelection
        for model in self._stack:
            if isinstance(model, QtGui.QAbstractProxyModel):
                proxySelection = model.mapSelectionFromSource(proxySelection)
        return proxySelection

    def sourceItem ( self, proxyIndex ):
        """
        Converts an model selection to the corresponding proxy selection.
        """
        proxySelection = sourceSelection
        for model in self._stack:
            if isinstance(model, QtGui.QAbstractProxyModel):
                proxySelection = model.mapSelectionFromSource(proxySelection)
        return proxySelection

    def select(self, condition = lambda x : True):
        """
        Sets the current selection in the view.

        @condition A lambda expression to be evaluated on each item.
        """ 
        self.selectedItems = [item for item in self.items if condition(item)]

class FilteredList(FilteredView):
    """
    The FilteredList class provides specialised FilterView with a ListView widget.
    """
    def __init__(self, parent=None, model = None, proxy = None):
        super(FilteredList, self).__init__(QtGui.QListView(), parent)
        self.setWindowTitle("Filtered List")

class FilteredTree(FilteredView):
    """
    The FilteredTree class provides specialised FilterView with a TreeView widget.
    """
    def __init__(self, parent=None):
        super(FilteredTree, self).__init__(TreeView(), parent)
        self.setWindowTitle("Filtered Tree")

class FilteredTable(FilteredView):
    """
    The FilteredTable class provides specialised FilterView with a TableView widget.
    """
    def __init__(self, parent=None):
        super(FilteredTable, self).__init__(QtGui.QTableView(), parent)
        self.setWindowTitle("Filtered Table")

if __name__ == "__main__":

    import sys, os, pprint
    from core.abstractmodel import AbstractDataListModel, AbstractDataItem
    from core.abstractmodel import AbstractDataTreeModel, AbstractDataTreeItem
    from core.abstractmodel import AbstractDataTableModel
    from core.proxymodel import ColumnFilterProxyModel, TreeColumnFilterProxyModel, ColumnFilterDataProxyModel

    class ExampleDataItem(AbstractDataItem):
        def __init__(self, data=[], parent=None):
            super(ExampleDataItem, self).__init__(data, parent)
        
        def data(self, id, role=QtCore.Qt.DisplayRole):
        
            if role == QtCore.Qt.DisplayRole:
                return "{0},{1}".format(self.row(), id)

            return super(ExampleDataItem, self).data(id, role)

        def size(self):
            return ExampleDataTreeModel.TotalColumns

    class ExampleDataListModel(AbstractDataListModel):

        def __init__(self, data, parent=None):
            super(ExampleDataListModel, self).__init__(parent)       

        def createItem(self, *args):
            return ExampleDataItem(*args)

        def reload(self, *args):
            self.beginResetModel()
            self.clear()
            for i in range(2):
                self.appendItem(ExampleDataItem( [], self ))
            self.endResetModel()

    class ExampleDataTableModel(AbstractDataTableModel):
        TotalColumns = 10

        def __init__(self, data, parent=None):
            super(ExampleDataTableModel, self).__init__(data, {}, parent)       

        def createItem(self, *args):
            return ExampleDataItem(*args)

        def reload(self, *args):
            self.beginResetModel()
            self.clear()
            for i in range(2):
                self.appendItem(ExampleDataItem( [], self ))
            self.endResetModel()

    class ExampleDataListModel(AbstractDataListModel):
        TotalColumns = 4

        def __init__(self, data, parent=None):
            super(ExampleDataListModel, self).__init__(parent)       

        def createItem(self, *args):
            return ExampleDataItem(*args)

        def reload(self, *args):
            self.beginResetModel()
            self.clear()
            for i in range(2):
                self.appendItem(ExampleDataItem( [], self ))
            self.endResetModel()

    class ExampleDataTreeItem(AbstractDataTreeItem):
        def __init__(self, data=[], parent=None):
            super(ExampleDataTreeItem, self).__init__(data, parent)
        
            self._databuffer = 4

        def data(self, id, role=QtCore.Qt.DisplayRole):
        
            if self.isRoot():
                return super(ExampleDataTreeItem, self).data(id, role)

            if role == QtCore.Qt.DisplayRole:
                return str(self.row()) if self.parent().isRoot() else "{0}_({1}_{2})".format(self.parent().data(id, role), str(self.row()), str(id))

            return super(ExampleDataTreeItem, self).data(id, role)

        def size(self):
            return ExampleDataTreeModel.TotalColumns

        def hasChildren(self):
            return self._databuffer > 0

        def canFetchMore(self):
            return self.childCount() < self._databuffer

        def fetchAmount(self):
            return 1 if self.canFetchMore() else 0

        def fetchMore(self):
            for i in range(0, self.fetchAmount()):
                self.appendChild(ExampleDataTreeItem([], self))

    class ExampleDataTreeModel(AbstractDataTreeModel):
        TotalColumns = 4

        def __init__(self, data, parent=None):
            super(ExampleDataTreeModel, self).__init__(data, parent)       

        def createRoot(self, *args):
            return ExampleDataTreeItem(*args)

        def createItem(self, *args):
            return ExampleDataTreeItem(*args)

        def reload(self, *args):
            pass

        def hasChildren(self, parent = QtCore.QModelIndex()):
            parentItem = self.item(parent)
            return parentItem.hasChildren()

        def canFetchMore(self,  parent = QtCore.QModelIndex()):
            parentItem = self.item(parent)
            return parentItem.canFetchMore()

        def fetchMore(self, parent = QtCore.QModelIndex()):
            parentItem = self.item(parent)
            curItems = parentItem.childCount()
            newItems = parentItem.fetchAmount()
            self.beginInsertRows(parent, curItems,  curItems + newItems - 1)
            parentItem.fetchMore()
            self.endInsertRows()

    app = QtGui.QApplication.instance()
    if not app: app = QtGui.QApplication([])

    # Tree Example: 
    # Tree View -> Data Proxy -> Filter Proxy -> Tree Model
    tree = FilteredTree()
    tree.push(ExampleDataTreeModel(["Tree Header {0}".format(i) for i in range(ExampleDataTreeModel.TotalColumns)]))
    tree.push(TreeColumnFilterProxyModel())
    tree.proxy.setFilterKeyColumn(-1)
    tree.push(ColumnFilterDataProxyModel())
    tree.proxy.setFilterData(QtCore.Qt.BackgroundRole, QtGui.QBrush(QtGui.QColor(224,91,49)))  #orange
    tree.proxy.setFilterData(QtCore.Qt.ForegroundRole, QtGui.QBrush( QtGui.QColor(0,0,0) ))  #not orange    
    tree.proxy.setFilterKeyColumn(-1)
    tree.label = "Example Tree"
    tree.immediate = False

    # List Example:
    # ListTree View -> Filter Proxy -> Filter Model
    list = FilteredList()
    list.push(ExampleDataListModel(["List Header"]))
    list.push(ColumnFilterProxyModel())
    list.label = "Example List"
    list.reloadable = True
    list.show()

    # List Example:
    # ListTree View -> Filter Proxy -> Filter Model
    table = FilteredTable()   
    table.push(ExampleDataTableModel(["Table Header {0}".format(i) for i in range(ExampleDataTableModel.TotalColumns)]))
    table.push(ColumnFilterProxyModel())
    table.proxy.setFilterKeyColumn(-1)
    table.proxy.setFilterRole(QtCore.Qt.DisplayRole)
    table.push(ColumnFilterDataProxyModel())
    table.proxy.setFilterData(QtCore.Qt.BackgroundRole, QtGui.QBrush( QtGui.QColor(255,255,128)))  #yellow
    table.proxy.setFilterData(QtCore.Qt.DisplayRole, "FILTER!")
    table.proxy.setFilterData(QtCore.Qt.DecorationRole, app.style().standardIcon(QtGui.QStyle.SP_MessageBoxWarning) )
    table.proxy.setFilterKeyColumn(-1)
    table.label = "Example Table"
    table.show()

    app.exec_()
