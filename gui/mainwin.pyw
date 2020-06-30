
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import Qt

from .win import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 禁止改变窗口大小
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint)
        self.setFixedSize(self.width(), self.height())
        # 按钮事件
        self.ui.btn_export_key.clicked.connect(  )
        self.ui.btn_import_key.clicked.connect(  )
        self.ui.btn_mining.clicked.connect(  )
        self.ui.btn_add_output.clicked.connect(  )
        self.ui.btn_broad_trans.clicked.connect(  )


