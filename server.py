"""
--- Servidor ---

Este código implementará a instância do servidor da aplicação
"""

import socket
import threading
import time
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
        continue

    print(f'[DESCONEXÃO] {addr} desconectado...')
    conn.close()


def inciar() -> None:
    """
    Inicia o servidor
    """
    server.listen()
    print(f'[AGUARDANDO CONEXÕES] Servidor esperando conexões em: {SERVER}\n')
    VEZ = 0
    PARES_ENCONTRADOS = 0
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

    while PARES_ENCONTRADOS < TOTAL_DE_PARES:
        for conn in CONEXOES_ATIVAS:
            string = imprime_status(TABULEIRO, PLACAR, VEZ)
            infos = {
                'msg': string,
                'vez': VEZ
            }
            envia_mensagem(str(infos), conn)
        jogada, KEEP_ALIVE = recebe_mensagem(CONEXOES_ATIVAS[VEZ])
        coordenadas = le_coordenada(DIM, jogada)

        i_1, j_1 = coordenadas

        abre_peca(TABULEIRO, i_1, j_1)
        for conn in CONEXOES_ATIVAS:
            string = imprime_status(TABULEIRO, PLACAR, VEZ)
            infos = {
                'msg': string,
                'vez': VEZ
            }
            envia_mensagem(str(infos), conn)
        jogada, KEEP_ALIVE = recebe_mensagem(CONEXOES_ATIVAS[VEZ])
        coordenadas = le_coordenada(DIM, jogada)

        i_2, j_2 = coordenadas
        abre_peca(TABULEIRO, i_2, j_2)
        
        if TABULEIRO[i_1][j_1] == TABULEIRO[i_2][j_2]:

            incrementa_placar(PLACAR, VEZ)

            for conn in CONEXOES_ATIVAS:
                string = imprime_status(TABULEIRO, PLACAR, VEZ)
                string += f"\nPecas casam! Ponto para o jogador {VEZ + 1}.\n"
                infos = {
                    'msg': string,
                    'vez': VEZ
                }
                envia_mensagem(str(infos), conn)
            PARES_ENCONTRADOS = PARES_ENCONTRADOS + 1
            remove_peca(TABULEIRO, i_1, j_1)
            remove_peca(TABULEIRO, i_2, j_2)

        else:
            for conn in CONEXOES_ATIVAS:
                string = imprime_status(TABULEIRO, PLACAR, VEZ)
                string += "\nPecas nao casam!\n"
                infos = {
                    'msg': string,
                    'vez': VEZ
                }
                envia_mensagem(str(infos), conn)
            fecha_peca(TABULEIRO, i_1, j_1)
            fecha_peca(TABULEIRO, i_2, j_2)
            VEZ = (VEZ + 1) % N_JOGADORES
            

            


limpa_tela()
print('[LIGADO] Servidor iniciando...\n')
inciar()
