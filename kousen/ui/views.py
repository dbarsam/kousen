from PySide import QtGui, QtCore

class TreeView(QtGui.QTreeView):
    """!
    TreeView extends the PySide QtGui.QTreeView object.
    """
    currentSelectionChanged = QtCore.Signal(object, object)

    def __init__(self, parent=None):
        """
        Constructor
        """
        super(TreeView, self).__init__(parent)

    def selectionChanged(self, selected, deselected):
        """
        Override the QtGui.QTreeView selectionChanged() method.

        @param selected   The new selection (which may be empty)
        @param deselected The previous selection (which may be empty)
        """
        self.currentSelectionChanged.emit(selected, deselected)

        super(TreeView, self).selectionChanged(selected, deselected)

