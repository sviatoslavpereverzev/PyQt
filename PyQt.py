import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from configparser import ConfigParser
import socket
import pickle


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        btn1 = QPushButton("Connect", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Send", self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.connect)
        btn2.clicked.connect(self.send)

        self.statusBar()

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Connect&Send')
        self.show()

    def connect(self):
        cfg = ConfigParser()
        cfg.read('settings.ini')
        HOST = cfg.get('server', 'host')
        PORT = int(cfg.get('server', 'port'))

        self.sock = socket.socket()
        self.sock.connect((HOST, PORT))
        self.statusBar().showMessage('Connect')

    def send(self):
        my_dict = {"id": 2, "name": "abc"}
        try:
            self.sock.send(pickle.dumps(my_dict))
            self.statusBar().showMessage('Send')
        except AttributeError:
            self.statusBar().showMessage('First click on connect')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
