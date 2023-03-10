# -*- coding: utf-8 -*-
import json
# Form implementation generated from reading ui file '阅读器.ui'
# Created by: PyQt5 UI code generator 5.15.9


import os
import shutil
import sys
from random import randint
import requests
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCursor, QColor
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QHeaderView, QTableWidgetItem, \
    QAbstractItemView, QPushButton
from lxml import etree
from qt_material import apply_stylesheet
from qframelesswindow import FramelessWindow, TitleBar
from PyQt5 import QtCore, QtWidgets
from functools import partial
from thread_reader import New_Thread, Requests_Thread


class CustomTitleBar(TitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)
        # customize the style of title bar button
        self.minBtn.setHoverColor(Qt.white)
        self.minBtn.setHoverBackgroundColor(QColor(0, 100, 182))
        self.minBtn.setPressedColor(Qt.white)
        self.minBtn.setPressedBackgroundColor(QColor(54, 57, 65))
        self.maxBtn.close()  # 取消最大化按钮


class Ui_Form(FramelessWindow, QWidget):
    def __init__(self, conf):
        super(Ui_Form, self).__init__()
        # 加载配置文件
        self.conf = conf
        self.setWindowTitle("PyQt-Frameless-Window")
        self.setTitleBar(CustomTitleBar(self))
        self.titleBar.raise_()
        self.titleBar.resize(0, 0)
        self.setFocusPolicy(Qt.StrongFocus)
        # 关闭调整大小
        self._isResizeEnabled = False
        self.setObjectName("Form")
        self.resize(200, 290)
        self.setFixedSize(200, 290)
        # 启动爬虫
        if self.conf.get("Is_Online"):
            self.thread = Requests_Thread()
            self.thread.start()
        # 背景1
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.W1 = QtWidgets.QWidget(self)
        self.W1.setGeometry(QtCore.QRect(0, 25, 310, 280))
        self.W1.setObjectName("W1")
        self.P1_ = QtWidgets.QPushButton(self.W1)  # 开始阅读
        self.P1_.setGeometry(QtCore.QRect(50, 30, 100, 40))
        self.P1_.setObjectName("P1_")
        self.P1_.clicked.connect(self.slot_btn_return_w2)

        self.P2_ = QtWidgets.QPushButton(self.W1)  # 在线阅读
        self.P2_.setGeometry(QtCore.QRect(50, 90, 100, 40))
        self.P2_.setObjectName("P2_")
        self.P2_.clicked.connect(self.slot_btn_return_w4)
        self.P3_ = QtWidgets.QPushButton(self.W1)  # 使用说明
        self.P3_.setGeometry(QtCore.QRect(50, 150, 100, 40))
        self.P3_.clicked.connect(self.slot_btn_return_w5)
        self.P3_.setObjectName("P3_")
        self.P4_ = QtWidgets.QPushButton(self.W1)  # 退出阅读
        self.P4_.setGeometry(QtCore.QRect(50, 210, 100, 40))
        self.P4_.setObjectName("P4_")
        self.P4_.clicked.connect(self.slot_btn_quit)
        # 背景2
        self.W2 = QtWidgets.QWidget(self)
        self.W2.setGeometry(QtCore.QRect(0, 25, 310, 330))
        # self.W2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.W2.setObjectName("W2")
        self.t1 = QtWidgets.QTableWidget(self.W2)  # 表格
        self.t1.setGeometry(QtCore.QRect(-15, 80, 310, 191))
        self.t1.setObjectName("tableWidget")
        # self.t1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)`
        self.t1.setColumnCount(3)
        self.t1.setRowCount(10)
        self.t1.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不能编辑
        self.t1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.t1.verticalHeader().setVisible(False)
        item = QtWidgets.QTableWidgetItem()
        self.t1.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.t1.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.t1.setHorizontalHeaderItem(2, item)
        # 初始化T1数据
        self.row, self.col, self.text, self.ssay, self.circulate = 0, 0, "", "", False
        self.t1.itemClicked.connect(self.t1_show_data)

        self.W2_P1 = QtWidgets.QPushButton(self.W2)  # 添加
        self.W2_P1.setGeometry(QtCore.QRect(10, 20, 75, 40))
        self.W2_P1.setObjectName("W2_P1")
        self.W2_P1.clicked.connect(self.slot_open_w2_p1)  # 返回W1

        self.W2_P2 = QtWidgets.QPushButton(self.W2)  # 删除
        self.W2_P2.setGeometry(QtCore.QRect(110, 20, 75, 40))
        self.W2_P2.setObjectName("W2_P2")
        self.W2_P2.clicked.connect(self.slot_delete_w2_p2)  # 删除表格

        self.W2_P3 = QtWidgets.QPushButton(self.W2)  # 返回
        self.W2_P3.setGeometry(QtCore.QRect(210, 20, 75, 40))
        self.W2_P3.setObjectName("W2_P3")
        self.W2_P3.clicked.connect(self.slot_btn_return_w1)  # 返回W1
        # 桌面三
        self.W3 = QtWidgets.QWidget(self)
        self.W3.setGeometry(QtCore.QRect(0, 25, 1000, 150))
        self.W3.setObjectName("W3")
        self.W3_R1 = QtWidgets.QTextBrowser(self.W3)  # 阅读器
        self.W3_R1.setGeometry(QtCore.QRect(25, 0, 970, 130))
        self.W3_R1.setObjectName("textBrowser")
        self.W3_R1.setReadOnly(True)  # 设置只读
        self.W3_R1.setTextInteractionFlags(Qt.NoTextInteraction)  # 设置不可点击
        self.W3_R1.setStyleSheet("background:transparent;border-width:0;border-style:outset;color:{};".format(
            self.conf.get("Font_Color")))  # 设置无边框

        # 桌面四
        self.W4 = QtWidgets.QWidget(self)
        self.W4.setGeometry(QtCore.QRect(0, 25, 460, 490))
        self.W4.setObjectName("W4")
        self.W4_B1 = QtWidgets.QPushButton(self.W4)
        self.W4_B1.setGeometry(QtCore.QRect(40, 60, 380, 60))
        self.W4_B1.permalink = "https://www.003kk.top/index.php/archives/39/"
        self.W4_B1.clicked.connect(partial(self.slot_w4_into_w3, self.W4_B1))

        self.W4_B1.setStyleSheet(
            "color: rgb(0, 0, 0);text-align:left;font: 75 10pt 宋体;background-image: url(./asset/1.jpg);background-position: right;")
        self.W4_B1.setObjectName("W4_B1")
        self.W4_B2 = QtWidgets.QPushButton(self.W4)
        self.W4_B2.permalink = "https://www.003kk.top/index.php/archives/37/"
        self.W4_B2.setGeometry(QtCore.QRect(40, 140, 380, 60))
        self.W4_B2.setStyleSheet(
            "color: rgb(0, 0, 0);text-align:left;font: 75 10pt 宋体;background-image: url(./asset/7.jpg);background-position: right;")
        self.W4_B2.clicked.connect(partial(self.slot_w4_into_w3, self.W4_B2))
        self.W4_B2.setObjectName("W4_B2")
        self.W4_B3 = QtWidgets.QPushButton(self.W4)
        self.W4_B3.permalink = "https://www.003kk.top/index.php/archives/36/"
        self.W4_B3.setGeometry(QtCore.QRect(40, 220, 380, 60))
        self.W4_B3.setStyleSheet(
            "color: rgb(0, 0, 0);text-align:left;font: 75 10pt 宋体;background-image: url(./asset/3.jpg);background-position: right;")
        self.W4_B3.clicked.connect(partial(self.slot_w4_into_w3, self.W4_B3))
        self.W4_B3.setObjectName("W4_B3")
        self.W4_B4 = QtWidgets.QPushButton(self.W4)
        self.W4_B4.permalink = "https://www.003kk.top/index.php/archives/34/"
        self.W4_B4.setGeometry(QtCore.QRect(40, 300, 380, 60))
        self.W4_B4.setStyleSheet(
            "color: rgb(0, 0, 0);text-align:left;font: 75 10pt 宋体;background-image: url(./asset/4.jpg);background-position: right;")
        self.W4_B4.clicked.connect(partial(self.slot_w4_into_w3, self.W4_B4))
        self.W4_B4.setObjectName("W4_B4")
        self.W4_B5 = QtWidgets.QPushButton(self.W4)
        self.W4_B5.permalink = "https://www.003kk.top/index.php/archives/33/"
        self.W4_B5.setGeometry(QtCore.QRect(40, 380, 380, 60))
        self.W4_B5.setStyleSheet(
            "color: rgb(0, 0, 0);text-align:left;font: 75 10pt 宋体;background-image: url(./asset/5.jpg);background-position: right;")
        self.W4_B5.clicked.connect(partial(self.slot_w4_into_w3, self.W4_B5))
        self.W4_B5.setObjectName("W4_B5")
        self.W4_B6 = QtWidgets.QPushButton(self.W4)  # 随机按钮
        self.W4_B6.setGeometry(QtCore.QRect(360, 5, 60, 40))
        # self.W4_B6.setIcon(QIcon(":/asset/洗牌_shuffle-one (2).png;"))
        self.W4_B6.clicked.connect(self.random_title)  # 返回W1
        self.W4_B6.setStyleSheet(r"image: url(./asset/random.png);")
        self.W4_B6.setText("")
        self.W4_B6.setObjectName("pushButton")

        self.W4_B7 = QtWidgets.QPushButton(self.W4)  # 返回按钮
        self.W4_B7.setGeometry(QtCore.QRect(280, 5, 62, 40))
        # self.W4_B6.setIcon(QIcon(":/asset/洗牌_shuffle-one (2).png;"))
        self.W4_B7.setStyleSheet(r"image: url(./asset/back.webp);")
        self.W4_B7.clicked.connect(self.slot_btn_return_w1)  # 返回W1
        self.W4_B7.setText("")
        self.W4_B7.setObjectName("pushButton")

        self.W4_BAR = QtWidgets.QProgressBar(self.W4)
        self.W4_BAR.setGeometry(QtCore.QRect(0, 455, 460, 10))
        self.W4_BAR.setProperty("value", 0)
        self.W4_BAR.setObjectName("progressBar")
        self.W4_BAR.setRange(0, 100)
        # self.W4_BAR.hide()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)
        self.W5 = QtWidgets.QWidget(self)
        self.W5.setGeometry(QtCore.QRect(0, 25, 460, 605))
        self.W5.setObjectName("widget")
        self.W5_T = QtWidgets.QTextEdit(self.W5)
        self.W5_T.setReadOnly(True)  # 设置只读
        self.W5_T.setTextInteractionFlags(Qt.NoTextInteraction)  # 设置不可点击
        self.W5_T.setGeometry(QtCore.QRect(0, 60, 460, 520))
        self.W5_T.setObjectName("textEdit")
        self.W5_B1 = QtWidgets.QPushButton(self.W5)  # 返回按钮
        self.W5_B1.setGeometry(QtCore.QRect(400, 8, 60, 40))
        # self.W4_B6.setIcon(QIcon(":/asset/洗牌_shuffle-one (2).png;"))
        self.W5_B1.setStyleSheet(r"image: url(./asset/back.webp);")
        self.W5_B1.clicked.connect(self.slot_btn_return_w1)  # 返回W1
        self.W5_B1.setText("")
        self.W5_B1.setObjectName("pushButton")

        # 设置T1的文件名
        self.t1_Name = ""

        # 设置W3是否置顶
        self.W3_Show = False

        self.retranslateUi(self)
        # 设置初始表格的行数
        self._hang = 0
        # self
        QtCore.QMetaObject.connectSlotsByName(self)
        # 先置顶W1
        self.W1.raise_()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.P1_.setText(_translate("Form", "开始阅读"))
        self.P2_.setText(_translate("Form", "在线阅读"))
        self.P3_.setText(_translate("Form", "使用说明"))
        self.P4_.setText(_translate("Form", "退出阅读"))

        self.t1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.t1.verticalHeader().setHidden(True) # 取消序号
        item = self.t1.horizontalHeaderItem(0)
        item.setText(_translate("Form", "书名"))
        item = self.t1.horizontalHeaderItem(1)
        item.setText(_translate("Form", "作者"))
        item = self.t1.horizontalHeaderItem(2)
        item.setText(_translate("Form", ""))
        self.W2_P1.setText(_translate("Form", "添加"))
        self.W2_P2.setText(_translate("Form", "删除"))
        self.W2_P3.setText(_translate("Form", "返回"))
        self.W4_B1.setText(_translate("Form", "重生\n{}2023年03月06日100阅读0评论0点赞".format("\t" * 19)))
        self.W4_B2.setText(_translate("Form", "李爷爷\n{}2023年03月06日10阅读0评论0点赞".format("\t" * 19)))
        self.W4_B3.setText(_translate("Form", "命运日记本\n{}2023年03月06日10阅读0评论0点赞".format("\t" * 19)))
        self.W4_B4.setText(_translate("Form", "偏心的婆婆\n{}2023年03月06日10阅读0评论0点赞".format("\t" * 19)))
        self.W4_B5.setText(_translate("Form", "和校霸互换身体后\n{}2023年03月06日10阅读0评论0点赞".format("\t" * 19)))
        self.W5_T.setHtml(_translate("Form",
                                     "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                     "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                     "p, li { white-space: pre-wrap; }\n"
                                     "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                     "<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">阅读功能说明</span></p>\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#00ff00;\">阅读功能支持添加本地书籍和在线书籍</span></p>\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">本地书籍</span></p>\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#aaaa7f;\">本地书籍只支持txt文件，点击开始阅读后在书架界面点添加然后按步骤完成添加即可</span></p>\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">在线书籍</span></p>\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; color:#aaaa7f;\">003kk.top免费盐选网是一个可以免费看知乎付费推文的小说站我们都会同步更新的 且免费盐选网不用花如何钱也没有广告完全可以免费观看 每天都稳定更新10篇+ 不用担心不更新,假如是点击不了,有可能是没加载出来哦🤭</span></p>\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">自定义设置说明(conf.json)</span></p>\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#00ffff;\">&quot;Theme&quot;:主题, 默认&quot;dark_lightgreen.xml&quot;</span></p>\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#00ffff;\">&quot;Is_Online&quot;: 是否在线 默认为true</span></p>\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#00ffff;\">&quot;Speed&quot;: 翻译速度, 默认2秒翻一次页</span></p>\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#00ffff;\">&quot;Font_Color&quot;:字体颜色, 默认绿色</span><br /><span style=\" font-size:12pt; font-weight:600;\">快捷键</span></p>\n"
                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#aaaaff;\">上一页：上一页，默认快捷键[W]或者[Ctrl+↑]或者[↑]。</span></p>\n"
                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#aaaaff;\">下一页：下一页，默认快捷键[S]或者[Ctrl+↓]或者[↓]。</span></p>\n"
                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#aaaaff;\">自动翻页开始与停止：启动或暂停自动翻页，默认快捷键[E]。</span></p>\n"
                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#aaaaff;\">老板键：一键退出，默认快捷键[Q]。</span></p>\n"
                                     "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">作者:lengleng </span><span style=\" font-family:\'Courier New\'; font-weight:600; font-style:italic; color:#ffffff;\"> </span><span style=\" font-family:\'Courier New\'; color:#ffffff;\">@Git: Aloof-0</span></p></body></html>"))

    # W4_B6随机获取
    def random_title(self):
        _translate = QtCore.QCoreApplication.translate

        with open("conf/html.json", "r", encoding="UTF-8") as f:
            js = json.loads(json.loads(json.dumps(f.read())))

        for s in [self.W4_B1, self.W4_B2, self.W4_B3, self.W4_B4, self.W4_B5]:
            ran_num = randint(1, len(js) - 1)
            s.setText(
                _translate("From", "{}\n{}{}".format(js[ran_num].get("title"), "\t" * 19, js[ran_num].get("column"))))
            s.setStyleSheet(
                "color: rgb(0, 0, 0);text-align:left;font: 75 10pt 宋体;background-image: url(./asset/{});background-position: right;".format(
                    js[ran_num].get("image_local")))
            s.permalink = js[ran_num].get("permalink")

    def update_progress(self):
        value = self.W4_BAR.value() + 1
        if value > 100:
            value = 0
        self.W4_BAR.setValue(value)

    def slot_btn_return_w5(self):

        self.W5.raise_()
        self.resize(460, 605)
        self.setFixedSize(460, 605)

    def slot_w4_into_w3(self, btn):
        self.W4_BAR.show()
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,xh;q=0.8,zh-TW;q=0.7",
            "Origin": "https://www.003kk.top",
            "Referer": "https://www.003kk.top",
            "Connection": "keep-alive"
        }
        html = requests.get(url=btn.permalink, headers=headers)
        self.W3_R1.setText("\n".join(etree.HTML(html.text).xpath("//article//text()")))
        self.W3_Show = True
        self.W3.raise_()
        self.resize(1000, 150)
        self.setFixedSize(1000, 150)

    # W1_P2 点击进入W4
    def slot_btn_return_w4(self):
        self.resize(460, 490)
        self.setFixedSize(460, 490)
        self.W4.raise_()

    # W1_P1 点击进入W2
    def slot_btn_return_w2(self):
        # self.t1.setVerticalHeaderLabels(('第一行', '第二行'))  # 这里使用元组，有几行或者几列，元组内有几个字符串
        _translate = QtCore.QCoreApplication.translate
        # 查看有多少份txt
        num = 0
        Chapman = os.path.join(self.cwd, "templates")
        for i in os.listdir(Chapman):
            de_path = os.path.join(Chapman, i)
            if os.path.isfile(de_path):
                if de_path.endswith(".txt"):  # Specify to find the txt file.
                    self.t1.setItem(num, 0, QTableWidgetItem(i.replace(".txt", "")))
                    self.t1.setColumnWidth(10, 10)
                    self.searchBtn = QPushButton('观看')
                    self.t1.setCellWidget(num, 2, self.searchBtn)
                    self.searchBtn.clicked.connect(self.DeleteButton)  # 删除表格
                    num += 1
                    self._hang += 1
        self.resize(295, 292)
        self.setFixedSize(295, 292)
        self.W2.raise_()

    # W2_P3 点击返回 W1
    def slot_btn_return_w1(self):
        self.resize(200, 290)
        self.setFixedSize(200, 290)
        self.W1.raise_()

    # W2_P1 点击新增书籍
    def slot_open_w2_p1(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "选取文件",
                                                                self.cwd,  # 起始路径
                                                                "Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔 # All Files (*);;Text Files (*.txt)

        if fileName_choose == "":
            print("\n取消选择")
            return

        print("\n你选择的文件为:")
        print(fileName_choose)
        # 迁移文件

        shutil.copy(fileName_choose,
                    os.path.join(os.path.join(os.getcwd(), "templates"), os.path.basename(fileName_choose)))

        # 表格添加一段/ 设置按钮
        self.t1.setItem(self._hang, 0, QTableWidgetItem(os.path.basename(fileName_choose).replace(".txt", "")))
        self.searchBtn1 = QPushButton('观看')
        self.searchBtn1.setDown(True)
        self.searchBtn1.setStyleSheet('QPushButton{margin:1px}')
        self.searchBtn1.clicked.connect(self.DeleteButton)  # 删除表格
        self.t1.setCellWidget(self._hang, 2, self.searchBtn1)
        self._hang += 1

    # W3_P2 删除书籍
    def slot_delete_w2_p2(self):
        # 删除T1 行数
        self.t1.removeRow(self.row)

        # 删除书记
        if self.text != "":
            os.remove(os.path.join(os.getcwd(), "templates/{}.txt".format(self.text)))

    # T1返回表格数据
    def t1_show_data(self, Item):
        if Item is None:
            return
        else:
            self.row = Item.row()  # 获取行数
            self.col = Item.column()  # 获取列数 注意是column而不是col哦
            self.text = Item.text()  # 获取内容
        print(self.row)

    # T1 返回表格按钮数据
    def DeleteButton(self):
        self.W3_Show = True  # 知道现在是W3
        button = self.sender()
        if button:
            # 确定位置的时候这里是关键
            row = self.t1.indexAt(button.pos()).row()
            column = self.t1.indexAt(button.pos()).column()
            # 获取文件名称
            print('单按钮位置: ', row, column)
            print(self.t1.item(row, 0).text())
            self.t1_Name = "{}.txt".format(self.t1.item(row, 0).text())
            self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明
            # 设置页面
            self.resize(1000, 150)
            self.setFixedSize(1000, 150)
            try:
                with open("templates/{}".format(self.t1_Name), "r", encoding='utf-8') as f:
                    k = f.read()
                    self.ssay = f.read()
            except Exception as e:
                with open("templates/{}".format(self.t1_Name), "r", encoding='ansi') as f:
                    k = f.read()
                    self.ssay = f.read()
            self.W3_R1.setText(k)
            self.W3.raise_()
            # 设置开始进度条q
            with open("conf/library.json", "r", encoding="utf8") as f:
                Yale = eval(f.read())
            self.W3_R1.verticalScrollBar().setValue(Yale.get("{}.txt".format(self.t1.item(row, 0).text())) if Yale.get(
                "{}.txt".format(self.t1.item(row, 0).text())) else 0)

    # 键盘快捷键
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            self.W3_R1.verticalScrollBar().setValue(self.W3_R1.verticalScrollBar().value() - 20)
            print(self.W3_R1.verticalScrollBar().value())
        if event.key() == Qt.Key_S:
            self.W3_R1.verticalScrollBar().setValue(self.W3_R1.verticalScrollBar().value() + 20)
            print(self.W3_R1.verticalScrollBar().value())

        if event.key() == Qt.Key_Q:
            self.__read_write_progress()
            QApplication.quit()
        # 自动循环播放
        if event.key() == Qt.Key_E:
            if not self.circulate:
                self.circulate = True
                self.thread = New_Thread(circulate=self.circulate, W3_R1=self.W3_R1, speed=self.conf.get("Speed"))
                self.thread.start()
            else:
                self.circulate = False
                self.thread.terminate()  # 终止线程

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 鼠标滑过
    def leaveEvent(self, e):  # 鼠标离开label
        if self.W3_Show:
            self.W3_R1.setStyleSheet("background:transparent;border-width:0;border-style:outset;")
            self.setWindowOpacity(0.3)  # 设置窗口透明度

    # 鼠标滑过
    def enterEvent(self, e):  # 鼠标离开label
        if self.W3_Show:
            self.W3_R1.setStyleSheet("background:transparent;border-width:0;border-style:outset;color:{};".format(
                self.conf.get("Font_Color")))
            self.setWindowOpacity(1)  # 设置窗口透明度

    # 退出事件
    def closeEvent(self, event):
        # 记住当前页面的进度, 存进json
        if self.W3_Show:
            self.__read_write_progress()

    # 设置一个私有函数读取文件进度
    def __read_write_progress(self):
        with open("conf/library.json", "r+", encoding="UTF-8") as f:
            _conf = eval(f.read())
            _conf[self.t1_Name] = self.W3_R1.verticalScrollBar().value()
            f.seek(0)
            f.truncate()
            f.write(json.dumps(_conf))

    # P4 退出
    def slot_btn_quit(self):
        QApplication.quit()


if __name__ == "__main__":
    with open("conf/conf.json", "r+", encoding="UTF8") as f:
        conf = json.loads(f.read())
    app = QApplication(sys.argv)
    mainForm = Ui_Form(conf)
    apply_stylesheet(app, theme=conf.get("Theme"))  # 样式
    # mainForm.setAttribute(Qt.WA_TranslucentBackground) # 设置透明背景
    # mainForm.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏窗口
    mainForm.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 置顶，且去掉边框
    mainForm.show()
    sys.exit(app.exec_())
