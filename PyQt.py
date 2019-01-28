# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import socket

connects = {}


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)

        self.host_text = QtWidgets.QTextEdit(Form)
        self.host_text.setGeometry(QtCore.QRect(330, 90, 161, 21))
        self.host_text.setObjectName("textEdit")

        self.clients_text = QtWidgets.QTextEdit(Form)
        self.clients_text.setGeometry(QtCore.QRect(40, 30, 261, 191))
        self.clients_text.setObjectName("clients_text")

        self.port_text = QtWidgets.QTextEdit(Form)
        self.port_text.setGeometry(QtCore.QRect(510, 90, 151, 21))
        self.port_text.setObjectName("port_text")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(670, 90, 61, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add)

        self.massege_text = QtWidgets.QTextEdit(Form)
        self.massege_text.setGeometry(QtCore.QRect(270, 260, 391, 21))
        self.massege_text.setObjectName("massege_text")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(670, 260, 61, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.send)

        self.log_text = QtWidgets.QTextEdit(Form)
        self.log_text.setGeometry(QtCore.QRect(40, 320, 691, 221))
        self.log_text.setObjectName("log_text")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 10, 60, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(330, 60, 60, 16))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(510, 60, 60, 16))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(330, 10, 91, 16))
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(40, 240, 60, 16))
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(150, 240, 91, 16))
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(270, 240, 60, 16))
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(40, 300, 60, 16))
        self.label_8.setObjectName("label_8")

        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(40, 260, 104, 26))
        self.comboBox.setObjectName("comboBox")

        self.comboBox_2 = QtWidgets.QComboBox(Form)
        self.comboBox_2.setGeometry(QtCore.QRect(150, 260, 104, 26))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItems(["ping", "status",
                                  "lower", "quit"])

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Add"))
        self.pushButton_2.setText(_translate("Form", "Send"))
        self.label.setText(_translate("Form", "Clients:"))
        self.label_2.setText(_translate("Form", "Host:"))
        self.label_3.setText(_translate("Form", "Port:"))
        self.label_4.setText(_translate("Form", "New client:"))
        self.label_5.setText(_translate("Form", "Client:"))
        self.label_6.setText(_translate("Form", "Request type:"))
        self.label_7.setText(_translate("Form", "Massege:"))
        self.label_8.setText(_translate("Form", "Log:"))

    def add(self):
        host = self.host_text.toPlainText()
        if not host:
            host = 'localhost'
        try:
            port = int(self.port_text.toPlainText())
            connects[str((host, port))] = socket.socket()
            try:
                connects[str((host, port))].connect((host, port))
                self.comboBox.addItem(str((host, port)))
                print(connects)
                self.clients_text.setText(f'Подключен:\n Host:{host} Port:{port}\n')
            except socket.gaierror:
                self.log_text.setText('Неизвесное host имя\n')
            except ConnectionRefusedError:
                self.log_text.setText('В соединении отказано\n')

        except ValueError:
            self.log_text.setText('Неправильное значение порта\n')

    def send(self):
        client = self.comboBox.currentText()
        request_type = self.comboBox_2.currentText()
        massage = self.massege_text.toPlainText()
        connects[client].send(bytes(f'{request_type}:{massage}\n', encoding='UTF-8'))
        data = connects[self.comboBox.currentText()].recv(1024)
        data = data.decode("utf-8")
        data = data.replace('\n', '').replace('\r', '')
        self.log_text.setText(data)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

