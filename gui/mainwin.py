import shutil
import json
import pyperclip
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from collections import defaultdict
from typing import Dict, List

from config import STORE_KEYS_FILE_PATH, WINDOW_ICON, WINDOW_TITLE
from chain import Btc
from key import UserKey
from peer import Wallet, Miner, FullBlockChain, NetworkRouting
from .win import Ui_MainWindow
from .timingevent import TimingEvent


__all__ = ["MainWindow", ]


class MainWindow(QMainWindow):
    """主窗口配置"""
    def __init__(self) -> None:
        super().__init__()
        self.pay_dict: Dict[str, Btc] = defaultdict(Btc)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon(WINDOW_ICON))
        # 禁止改变窗口大小
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint)
        self.setFixedSize(self.width(), self.height())
        # 按钮事件
        self.ui.btn_export_key.clicked.connect(self.__export_key)
        self.ui.btn_import_key.clicked.connect(self.__import_key)
        self.ui.btn_mining.clicked.connect(self.__mining_action)
        self.ui.btn_add_output.clicked.connect(self.__add_output)
        self.ui.btn_broad_trans.clicked.connect(self.__broad_trans)
        self.ui.btn_payments.clicked.connect(self.__collect)
        self.ui.btn_add_node.clicked.connect(self.__add_node)
        # 初始化面板
        node_list = NetworkRouting.get_instance().get_nodes()
        self.ui.node_list.addItems(node_list)
        # 定时事件
        self.nodelist_change = TimingEvent(lambda : NetworkRouting.get_instance().set_nodes(self.__get_node_list()))
        self.nodelist_change.startTimer(2000)
        self.balance_change = TimingEvent(lambda : self.ui.label_balance.setText(str(Wallet.get_instance().lookup_balance())))
        self.balance_change.startTimer(2000)
        self.height_change = TimingEvent(lambda : self.ui.label_block_height.setText(str(FullBlockChain.get_instance().get_height())))
        self.height_change.startTimer(2000)

    def __get_node_list(self) -> List[str]:
        """获取所有node_list"""
        tap = []
        for i in range(self.ui.node_list.count()):
            tap.append(self.ui.node_list.item(i).text().strip())
        return tap

    def __add_node(self) -> None:
        """添加网络节点"""
        self.ui.node_list.edit_new_item()

    def __collect(self) -> None:
        """收钱"""
        pyperclip.copy(Wallet.get_instance().collect())
        self.ui.pay_addr.setText("收钱地址已复制到剪贴板。。。")

    def __export_key(self) -> None:
        """导出秘钥"""
        path, _ = QFileDialog.getSaveFileName(self, "选择存储位置", ".", "秘钥文件(*.keys)")
        if path.strip():
            Wallet.get_instance().write_keys_to_file()
            shutil.copy(STORE_KEYS_FILE_PATH, path)

    def __import_key(self) -> None:
        """导入秘钥"""
        path, _ = QFileDialog.getOpenFileName(self, "选择秘钥文件", ".", "秘钥文件(*.keys)")
        try:
            Wallet.get_instance().import_keys_from_file(path)
        except Exception as e:
            print(e)

    def __mining_action(self) -> None:
        """开始挖矿或取消挖矿"""
        if self.ui.btn_mining.text() == "开始挖矿":
            self.ui.btn_mining.setText("停止挖矿")
            Miner.get_instance().start_server()
        else:
            self.ui.btn_mining.setText("开始挖矿")
            Miner.get_instance().close_server()
    
    def __add_output(self) -> None:
        """添加付费输出"""
        btcs = self.ui.box_pay_btcs.text()
        address = self.ui.line_pay_address.text()
        if UserKey.is_address(address):
            self.pay_dict[address] += Btc(btcs)
        tap = {}
        for key, value in self.pay_dict.items():
            tap[key] = str(value)
        self.ui.edit_trans.setText(json.dumps(tap, ensure_ascii=False, indent=2, separators=(',', ': ')))

    def __broad_trans(self) -> None:
        """付钱"""
        tap: Dict[str, Btc] = defaultdict(Btc)
        for key, value in self.pay_dict.items():
            if UserKey.is_address(key):
                tap[key] += value
        trans = Wallet.get_instance().pay(tap)
        Wallet.get_instance().broad_a_trans(trans)


    


