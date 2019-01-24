from time import sleep
import socket
import pickle
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('settings.ini')
HOST = cfg.get('server', 'host')
PORT = int(cfg.get('server', 'port'))

sock = socket.socket()
sock.connect((HOST, PORT))
dict = {"id": 1, "name": "abc"}

for i in range(10):
    sock.send(pickle.dumps(dict))
    sleep(0.5)

data = sock.recv(1024)
print(data)

sock.close()
