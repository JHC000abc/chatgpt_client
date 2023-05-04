# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :

"""
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from gui.ui.chat import Ui_Form
from threading import Thread
from gui.ctrl import net
import time
from settings.setting import *


class Chat(QtWidgets.QWidget):
    single_show_result = QtCore.pyqtSignal(str, int)
    single_clear_result = QtCore.pyqtSignal()
    single_status_search = QtCore.pyqtSignal(int)
    single_sleep = QtCore.pyqtSignal(int)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._slot()
        self._init()
        self._setting()

    def _init(self):
        self.result = None

    def _setting(self):
        self.ui.textEdit_out.setReadOnly(True)

        self.setMaximumSize(WIN["MAX_X"], WIN["MAX_Y"])
        self.setMinimumSize(WIN["MIN_X"], WIN["MIN_Y"])

        self.setWindowTitle(WIN["TITLE"])

        self.ui.pushButton_search.setFocus()
        self.ui.pushButton_search.setShortcut(
            QKeySequence.InsertParagraphSeparator)
        self.ui.pushButton_search.setShortcut(Qt.Key_Enter)
        self.ui.pushButton_search.setShortcut(Qt.Key_Return)
        self.ui.pushButton_search.setDefault(True)

    def _slot(self):
        self.ui.pushButton_search.clicked.connect(self.slot_search)
        self.single_show_result.connect(self.show_result)
        self.single_clear_result.connect(self.clear_result)
        self.single_status_search.connect(self.check_status_search)
        self.single_sleep.connect(self.single_sleep_times)

    def get_result(self, input):
        self.single_status_search.emit(1)
        result = net.get_result(input)
        if result:
            self.single_clear_result.emit()
            msg_head = self.input + " [搜索结果] :"
            self.single_show_result.emit(msg_head, 1)
            for st in result:
                self.single_show_result.emit(st, 0)
                time.sleep(SLEEP["OUT_STEP"])

        self.single_status_search.emit(0)

    def single_sleep_times(self, em):
        time.sleep(em)

    def check_status_search(self, em):
        if em == 1:
            self.ui.pushButton_search.setDisabled(True)
        else:
            self.ui.pushButton_search.setDisabled(False)

    def clear_result(self):
        self.ui.textEdit_out.clear()

    def show_result(self, result, mode):
        if mode == 0:
            now_text = self.ui.textEdit_out.toPlainText()
            self.ui.textEdit_out.setText(now_text + result)
        else:
            self.ui.textEdit_out.setText(result)
            self.ui.textEdit_out.append("\n")

    def slot_search(self):
        """

        """

        input = self.ui.textEdit_input.toPlainText()
        self.input = input.strip()
        if input != "":
            self.ui.textEdit_out.setText("正在全力搜索中……")
            self.t = Thread(target=self.get_result, args=(input,))
            self.t.setDaemon(True)
            self.t.start()
            self.ui.textEdit_input.clear()

        else:
            self.ui.textEdit_out.setText("请输入问题")
