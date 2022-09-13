"""Servidor

Este código implementará a instância do servidor da aplicação
"""

import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    """
    Lida com as conexões ao servidor
    """
    print(f'[NEW CONNECTION] {addr} connected...')

    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f'[{addr}] {msg}...')

    conn.close()


def start() -> None:
    """
    Inicia o servidor
    """
    server.listen()
    print(f'[LISTENING] server is listening on {SERVER}')

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}...')


print('[STARTING] server is starting...')
start()
