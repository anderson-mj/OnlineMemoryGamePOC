"""
--- Servidor ---

Este código implementará a instância do servidor da aplicação
"""

import socket
import threading
from utils import *
import json
import ast

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

"""
Configurações do jogo
"""

PARES_ENCONTRADOS = 0
CONEXOES_ATIVAS = []
TABULEIRO = novo_tabuleiro(DIM)
PLACAR = novo_placar(N_JOGADORES)
VEZ = 0


def gerencia_cliente(conn, addr):
    """
    Lida com as conexões ao servidor
    """
    KEEP_ALIVE = True
    while KEEP_ALIVE:
        infos, KEEP_ALIVE = recebe_mensagem(conn)
        infos = ast.literal_eval(infos)
        
        for conn in CONEXOES_ATIVAS:
            envia_mensagem(str(infos), conn)

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
            thread = threading.Thread(
                target=gerencia_cliente, args=(conn, addr))
            thread.start()
            CONEXOES_ATIVAS.append(conn)
            print(f'[NOVA CONEXÃO] {addr} conectado...')
            envia_mensagem(str(threading.active_count() - 1), conn)
        else:
            for conn in CONEXOES_ATIVAS:
                envia_mensagem('CAN_PLAY', conn)
            print(f'[LIMITE ATINGIDO] Limite de jogadores atingido...')
            break
    
    infos = {
        'tabuleiro': TABULEIRO,
        'placar': PLACAR,
        'vez': VEZ,
        'pares_encontrados': PARES_ENCONTRADOS
    }

    for conn in CONEXOES_ATIVAS:
        envia_mensagem(str(infos), conn)



limpa_tela()
print('[LIGADO] Servidor iniciando...\n')
inciar()
