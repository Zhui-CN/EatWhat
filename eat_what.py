# -*- coding: utf-8 -*-

import sys
import random
import time
import json
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QStringListModel
from PySide2.QtWidgets import QApplication
from threading import Thread


class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.node = None
        self.setupUi(self)
        self.list_eat_arr = []
        self.list_drink_arr = []
        self.initialization()

    def setupUi(self, Form):
        Form.resize(507, 367)
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 70, 219, 111))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.horizontalLayout_3.addWidget(self.label)

        self.line_random = QtWidgets.QLineEdit(self.layoutWidget)
        self.horizontalLayout_3.addWidget(self.line_random)

        self.pushButton_eat = QtWidgets.QPushButton(Form)
        self.pushButton_eat.clicked.connect(lambda: self.thread_run("eat"))
        self.pushButton_eat.setGeometry(QtCore.QRect(40, 210, 91, 71))

        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(280, 0, 221, 291))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.list_eat = QtWidgets.QListView(self.layoutWidget1)
        self.list_eat.clicked.connect(self.select_food_node)
        self.horizontalLayout_2.addWidget(self.list_eat)

        self.list_drink = QtWidgets.QListView(self.layoutWidget1)
        self.list_drink.clicked.connect(self.select_drink_node)
        self.horizontalLayout_2.addWidget(self.list_drink)

        self.pushButton_drink = QtWidgets.QPushButton(Form)
        self.pushButton_drink.clicked.connect(lambda: self.thread_run("drink"))
        self.pushButton_drink.setGeometry(QtCore.QRect(150, 210, 91, 71))

        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(280, 300, 221, 56))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.add_eat_Button = QtWidgets.QPushButton(self.widget)
        self.add_eat_Button.clicked.connect(lambda: self.add_goods("eat"))
        self.verticalLayout.addWidget(self.add_eat_Button)

        self.del_eat_Button = QtWidgets.QPushButton(self.widget)
        self.del_eat_Button.clicked.connect(lambda: self.del_goods("eat"))
        self.verticalLayout.addWidget(self.del_eat_Button)

        self.horizontalLayout.addLayout(self.verticalLayout)
        self.line_goods = QtWidgets.QLineEdit(self.widget)
        self.line_goods.setMaxLength(32767)
        self.horizontalLayout.addWidget(self.line_goods)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()

        self.add_drink_Button = QtWidgets.QPushButton(self.widget)
        self.add_drink_Button.clicked.connect(lambda: self.add_goods("drink"))
        self.verticalLayout_2.addWidget(self.add_drink_Button)

        self.del_drink_Button = QtWidgets.QPushButton(self.widget)
        self.del_drink_Button.clicked.connect(lambda: self.del_goods("drink"))
        self.verticalLayout_2.addWidget(self.del_drink_Button)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "今天吃啥喝啥"))
        self.label.setText(_translate("Form", "今天(吃/喝：)"))
        self.pushButton_eat.setText(_translate("Form", "开始吃"))
        self.pushButton_drink.setText(_translate("Form", "开始喝"))
        self.add_eat_Button.setText(_translate("Form", "添加食物"))
        self.del_eat_Button.setText(_translate("Form", "删除食物"))
        self.add_drink_Button.setText(_translate("Form", "添加饮料"))
        self.del_drink_Button.setText(_translate("Form", "删除饮料"))

    def select_food_node(self, index):
        self.line_goods.setText(self.list_eat_arr[index.row()])

    def select_drink_node(self, index):
        self.line_goods.setText(self.list_drink_arr[index.row()])

    def initialization(self):
        li = ["eat", "drink"]
        for l in li:
            item = self.get_item(l)
            listModel = QStringListModel()
            listModel.setStringList(item)
            model_1 = getattr(self, "list_{}".format(l))
            model_2 = getattr(self, "list_{}_arr".format(l))
            model_2.clear()
            model_2 += item
            model_1.setModel(listModel)

    def get_item(self, name):
        with open('{}.json'.format(name), 'r', encoding='utf-8') as f:
            data = json.load(f)["value"]
            return data

    def write_item(self, name, data):
        with open('{}.json'.format(name), 'w', encoding='utf-8') as f:
            json.dump({"value": data}, f, ensure_ascii=False)
        self.initialization()

    def add_item(self, name, data):
        model = getattr(self, "list_{}_arr".format(name))
        if data in model:
            self.line_goods.setText("物品已存在")
            return
        model.append(data)
        self.write_item(name, model)

    def del_item(self, name, data):
        model = getattr(self, "list_{}_arr".format(name))
        if data not in model:
            self.line_goods.setText("你输入的物品不存在")
            return
        model.remove(data)
        self.write_item(name, model)

    def random_goods(self, goods):
        lis = getattr(self, "list_{}_arr".format(goods))
        if lis:
            num = 10
            while num:
                li = random.choice(lis)
                time.sleep(0.1)
                self.line_random.setText(li)
                num -= 1

    def add_goods(self, goods):
        text = self.line_goods.text()
        if not text or self.line_goods.text().startswith("请输入") or "存在" in self.line_goods.text():
            self.line_goods.setText("请输入要添加的物品")
        else:
            self.add_item(goods, text)

    def del_goods(self, goods):
        text = self.line_goods.text()
        if not text or self.line_goods.text().startswith("请输入"):
            self.line_goods.setText("请输入要删除的物品")
        else:
            self.del_item(goods, text)

    def thread_run(self, goods):
        Thread(target=self.random_goods, args=(goods,)).start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    eat_gui = Ui_Form()
    eat_gui.show()
    sys.exit(app.exec_())
