import socket
from configparser import ConfigParser
from _thread import *
from time import time
import sys

clients = []


def get_settings():
    cfg = ConfigParser()
    cfg.read('settings.ini')
    host = cfg.get('server', 'host')
    listeners = int(cfg.get('server', 'listeners'))

    if len(sys.argv) > 1:
        port = (int(sys.argv[1]))
    else:
        port = int(cfg.get('server', 'port'))

    return {'host': host, 'port': port, 'listeners': listeners}


def new_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((list_cfg['host'], list_cfg['port']))
    sock.listen(list_cfg['listeners'])
    return sock


def client(conn):
    conn.send(bytes('Hello from server!\n', encoding='UTF-8'))
    while True:
        data = conn.recv(1024)
        data = data.decode("utf-8")
        data = data.replace('\n', '').replace('\r', '')
        data = data.split(':')
        try:
            if data[0] == 'ping' and data[1] == '*':
                conn.send(bytes('ping:+\n', encoding='UTF-8'))

            elif data[0] == 'status':
                reply = f'status:(time:{int(time())}, connections_count:{len(clients)}, ' \
                        f'available quantity: {list_cfg["listeners"]})\n'
                conn.send(bytes(reply, encoding='UTF-8'))

            elif data[0] == 'lower':
                lower_str = str(data[1]).lower()
                conn.send(bytes(f'lower:{lower_str}\n', encoding='UTF-8'))

            elif data[0] == 'quit':
                print(conn.getpeername())
                clients.remove(conn.getpeername())
                conn.send(bytes('quit\n', encoding='UTF-8'))
                break
            else:
                conn.send(bytes('not recognized\n', encoding='UTF-8'))
        except IndexError:
            conn.send(bytes('not recognized\n', encoding='UTF-8'))

        if not data:
            break
    conn.close()


if __name__ == '__main__':
    list_cfg = get_settings()
    my_sock = new_sock()

    while True:
        conn, addr = my_sock.accept()
        print('connected:', addr)
        if addr not in clients:
            clients.append(addr)
        start_new_thread(client, (conn,))
