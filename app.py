import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

from config import STORE_DIR
from peer import NetworkRouting, FullBlockChain, Wallet
from gui import MainWindow


if __name__ == '__main__':
    # 打开N服务和B服务，以及W服务
    NetworkRouting.get_instance().start_server()
    FullBlockChain.get_instance().start_server()
    Wallet.get_instance().start_server()
    # 显示GUI
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
    # 保存密钥
    Wallet.get_instance().write_keys_to_file()
