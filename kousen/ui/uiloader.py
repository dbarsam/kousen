import sys
import PySide
import pysideuic
import xml.etree.ElementTree as xml
from io import StringIO

from PySide.QtCore import QMetaObject
from PySide.QtUiTools import QUiLoader

class UiLoader(QUiLoader):
    """
    Subclass :class:`~PySide.QtUiTools.QUiLoader` to create the user interface
    in a base instance.

    Unlike :class:`~PySide.QtUiTools.QUiLoader` itself this class does not
    create a new instance of the top-level widget, but creates the user
    interface in an existing instance of the top-level class.

    This mimics the behaviour of :func:`PyQt4.uic.loadUi`.
    """

    def __init__(self, baseinstance):
        """
        Create a loader for the given ``baseinstance``.

        The user interface is created in ``baseinstance``, which must be an
        instance of the top-level class in the user interface to load, or a
        subclass thereof.

        ``parent`` is the parent object of this loader.
        """
        QUiLoader.__init__(self, baseinstance)
        self.baseinstance = baseinstance

    @classmethod
    def loadUiType(cls, uifile, respath=None):
        """
        Pyside lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
        and then execute it in a special frame to retrieve the form_class.
        """
        parsed = xml.parse(uifile)
        widget_class = parsed.find('widget').get('class')
        form_class = parsed.find('class').text

        with open(uifile, 'r') as f:
            o = StringIO()
            frame = {}

            pysideuic.compileUi(f, o, indent=0)
            pyc = compile(o.getvalue(), '<string>', 'exec')

            hasres = respath and respath not in sys.path
            if hasres:
                sys.path.append(respath)

            exec(pyc, frame)

            if hasres:
                sys.path.remove(respath)

            #Fetch the base_class and form class based on their type in the xml from designer
            form_class = frame['Ui_%s'%form_class]
            base_class = eval('PySide.QtGui.%s'%widget_class)
        return form_class, base_class

    @classmethod
    def loadUi(cls, uifile, baseinstance=None):
        """
        Dynamically load a user interface from the given ``uifile``.

        ``uifile`` is a string containing a file name of the UI file to load.

        If ``baseinstance`` is ``None``, the a new instance of the top-level widget
        will be created.  Otherwise, the user interface is created within the given
        ``baseinstance``.  In this case ``baseinstance`` must be an instance of the
        top-level widget class in the UI file to load, or a subclass thereof.  In
        other words, if you've created a ``QMainWindow`` interface in the designer,
        ``baseinstance`` must be a ``QMainWindow`` or a subclass thereof, too.  You
        cannot load a ``QMainWindow`` UI file with a plain
        :class:`~PySide.QtGui.QWidget` as ``baseinstance``.

        :method:`~PySide.QtCore.QMetaObject.connectSlotsByName()` is called on the
        created user interface, so you can implemented your slots according to its
        conventions in your widget class.

        Return ``baseinstance``, if ``baseinstance`` is not ``None``.  Otherwise
        return the newly created instance of the user interface.
        """
        loader = cls(baseinstance)
        widget = loader.load(uifile)
        QMetaObject.connectSlotsByName(widget)
        return widget

    def createWidget(self, class_name, parent=None, name=''):
        if parent is None and self.baseinstance:
            # supposed to create the top-level widget, return the base instance
            # instead
            return self.baseinstance
        else:
            # create a new widget for child widgets
            widget = QUiLoader.createWidget(self, class_name, parent, name)
            if self.baseinstance:
                # set an attribute for the new child widget on the base
                # instance, just like PyQt4.uic.loadUi does.
                setattr(self.baseinstance, name, widget)
            return widget

