# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author  : v_jiaohaicheng@baidu.com
@des     :

"""
import sys
from PyQt5 import QtWidgets
from gui.ctrl.Chat import Chat
from qt_material import apply_stylesheet
from settings.setting import *


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.processEvents()
    try:
        apply_stylesheet(app, theme=STYLE["THEME"])
    except:
        pass
    Form = Chat()
    Chat.show(Form)
    sys.exit(app.exec_())
