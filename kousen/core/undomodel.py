from PySide import QtGui, QtCore

class UndoMacro(object):
    """
    The UndoMacro class provides a Context Manager for Qt's Undo Macros.
    """
    def __init__(self, undostack, description=""):
        """
        Constructor.

        @param undostack The undostack.
        @param description The description text of the macro.
        """
        self._stack = undostack
        self._text = description

    def __enter__(self):
        """
        Start Undo Macro recording.
        """
        self._stack.beginMacro(self._text)

    def __exit__(self, atype, value, traceback):
        """
        Stop Undo Macro recording.
        """
        self._stack.endMacro()

class SetDataCommand(QtGui.QUndoCommand):
    """
    The SetDataCommand class implements a command to invoke the setData method of a QAbstractItemModel instance.
    """
    def __init__(self, index, value, role, model, text=None, parent=None):
        """
        Constructor.

        @param index       The QModelIndex.
        @param value       The value to be applied at the index.
        @param role        The role Qt Item Data Role of the index.
        @param model       The model.
        @param text        The QUndoCommand display text.
        @param parent      The QObject parent of the QUndoCommand
        """
        super(SetDataCommand, self).__init__(text, parent)
        self._model = model
        self._index = QtCore.QPersistentModelIndex(index)
        self._role = role
        self._oldvalue = index.data(role)
        self._newvalue = value
        if not text:
            self.setText("({0},{1}) => [{2}] to [{3}] Role: {4}".format(self._index.row(), self._index.column(), self._oldvalue, self._newvalue, next((n for n, r in QtCore.Qt.ItemDataRole.values.items() if r == role), "<Unknown>")))

    def redo(self):
        """
        Executes the apply action of the command.
        """
        super(SetDataCommand, self).redo()
        self._model.setData(self._index, self._newvalue, self._role)

    def undo(self):
        """
        Executes the cancel action of the command.
        """
        super(SetDataCommand, self).undo()
        self._model.setData(self._index, self._oldvalue, self._role)

class UndoRedoProxyModel(QtGui.QSortFilterProxyModel):
    """
    The UndoRedoProxyModel subclasses the QSortFilterProxyModel to provide undo|redo functionality via a Proxy Model.
    """
    def __init__(self, undostack = None, parent = None):
        """
        Constructor.

        @param undostack The undostack.
        @param parent    The QObject parent object.
        """
        super(UndoRedoProxyModel, self).__init__(parent)
        self._undostack = undostack or QtGui.QUndoStack(self)

    def undoModel(self):
        """
        Returns the undo stack being used by this model.
        """
        return self._undostack

    def setUndoModel(self, model):
        """
        Sets the undo stack being used by this model.
        """
        self._undostack = model   

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Sets the model data at a given index, filtered by the given role to the value.
        """
        if not index.isValid():
            return False

        if value == index.data(role):
            return False

        # Create a Command that invokes the Base Class
        command = SetDataCommand(index, value, role, super(UndoRedoProxyModel, self))
        self._undostack.push(command)
        return True
