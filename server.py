import socket
import pickle
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('settings.ini')
HOST = cfg.get('server', 'host')
PORT = int(cfg.get('server', 'port'))
LISTENERS = int(cfg.get('server', 'listeners'))
clients = []

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(LISTENERS)
conn, addr = sock.accept()


quit = False
print('connected:', addr)

while not quit:
    try:
        data = conn.recv(1024)
        data = pickle.loads(data)
        if addr not in clients:
            clients.append(addr)

    except EOFError:
        print('')

    print(data)



conn.close()
