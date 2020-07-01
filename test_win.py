import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

from config import STORE_DIR
from gui import MainWindow


if __name__ == '__main__':
    if not os.path.isdir(STORE_DIR):
        os.mkdir(STORE_DIR)
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
