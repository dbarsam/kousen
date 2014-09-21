import sys
import os
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) )

def main():
    """
    The main entry point for Kousen
    """
    import sys
    import PySide
    import resources_rc
    from ui.mainwindow import MainWindow

    app = PySide.QtGui.QApplication(['Kousen'])
    mainwindow = MainWindow()
    mainwindow.show()

    return app.exec_()

if __name__ == '__main__':
  sys.exit(main())
