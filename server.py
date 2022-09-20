"""
--- Servidor ---

Este código implementará a instância do servidor da aplicação
"""

import socket
import threading
from utils import *
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

"""
Configurações do jogo
"""
DIM = 4
N_JOGADORES = 2
TOTAL_DE_PARES = DIM**2 / 2
PARES_ENCONTRADOS = 0
CONEXOES_ATIVAS = []
TABULEIRO = novo_tabuleiro(DIM)
PLACAR = novo_placar(N_JOGADORES)

def gerencia_cliente(conn, addr):
    """
    Lida com as conexões ao servidor
    """
    KEEP_ALIVE = True
    while KEEP_ALIVE:
        mensagem, KEEP_ALIVE = recebe_mensagem(conn)
        print(mensagem)

    print(f'[DESCONEXÃO] {addr} desconectado...')
    conn.close()


def inciar() -> None:
    """
    Inicia o servidor
    """
    server.listen()
    print(f'[AGUARDANDO CONEXÕES] Servidor esperando conexões em: {SERVER}\n')

    while True:
        if threading.active_count() - 1 < N_JOGADORES:
            conn, addr = server.accept()
            thread = threading.Thread(target=gerencia_cliente, args=(conn, addr))
            thread.start()
            CONEXOES_ATIVAS.append(conn)
            print(f'[NOVA CONEXÃO] {addr} conectado...')
            envia_mensagem(str(threading.active_count() - 1), conn)
        else:
            for conn in CONEXOES_ATIVAS:
                envia_mensagem('CAN_PLAY', conn)
            print(f'[LIMITE ATINGIDO] Limite de jogadores atingido...')
            break

limpa_tela()
print('[LIGADO] Servidor iniciando...\n')
inciar()
