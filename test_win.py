import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from gui.win import Ui_MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(c)
    c.show()
    sys.exit(app.exec_())


