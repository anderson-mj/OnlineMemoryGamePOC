"""
--- Servidor ---

Este código implementará a instância do servidor da aplicação
"""

import socket
import threading
from utils import *
# import json

DIM = 4
N_JOGADORES = 2
TOTAL_DE_PARES = DIM**2 / 2
PARES_ENCONTRADOS = 0
VEZ = 0

active_connections = []


def handle_client(conn, addr):
    """
    Lida com as conexões ao servidor
    """
    print(f'[NOVA CONEXÃO] {addr} conectado...')

    connected = True
    while connected:
        connected = receive_message(conn)
        send_message('Mensagem do servidor', conn)

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
        active_connections.append(conn)
        print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}...\n\n')

        while not len(active_connections) == N_JOGADORES:
            for conn in active_connections:
                send_message('can_play: False', conn)

        send_message('can_play: True', conn)


print('[LIGADO] Servidor iniciando...')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

start()
