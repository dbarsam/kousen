import sys
import os
import PySide

def main():
    """
    The main entry point for Kousen
    """    
    import kousen.resources_rc
    from kousen.ui.mainwindow import MainWindow

    app = PySide.QtGui.QApplication(['Kousen'])
    app.setQuitOnLastWindowClosed(True)

    mainwindow = MainWindow()
    mainwindow.show()

    return app.exec_()

if __name__ == '__main__':
    packagepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if not packagepath in sys.path:
        sys.path.append(packagepath)
    sys.exit(main())