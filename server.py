"""
--- Servidor ---

Este código implementará a instância do servidor da aplicação
"""

import socket
import threading
from utils import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

KEEP_ALIVE = True
PARES_ENCONTRADOS = 0
CONEXOES_ATIVAS = []
TABULEIRO = novo_tabuleiro(DIM)
PLACAR = novo_placar(N_JOGADORES)


def gerencia_cliente(conn, addr):
    """
    Lida com as conexões ao servidor
    """
    while KEEP_ALIVE:
        continue

    print(f'[DESCONEXÃO] {addr} desconectado...')
    conn.close()


def iniciar() -> None:
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
            thread = threading.Thread(target=gerencia_cliente, args=(conn, addr))
            thread.start()
            CONEXOES_ATIVAS.append(conn)
            print(f'[NOVA CONEXÃO] {addr} conectado...\n')
            envia_mensagem(str(threading.active_count() - 1), conn)
        else:
            for conn in CONEXOES_ATIVAS:
                envia_mensagem('CAN_PLAY', conn)
            print(f'[LIMITE ATINGIDO] Limite de jogadores atingido...\n')
            break

    while PARES_ENCONTRADOS < TOTAL_DE_PARES:
        for conn in CONEXOES_ATIVAS:
            string = imprime_status(TABULEIRO, PLACAR, VEZ)
            infos = {
                'msg': string,
                'vez': VEZ
            }
            envia_mensagem(str(infos), conn)

        while True:
            jogada = recebe_mensagem(CONEXOES_ATIVAS[VEZ])
            coordenadas = le_coordenada(DIM, jogada)
            i_1, j_1 = coordenadas

            if abre_peca(TABULEIRO, i_1, j_1) is False:
                for conn in CONEXOES_ATIVAS:
                    string = imprime_status(TABULEIRO, PLACAR, VEZ)
                    string += "\nEscolha uma peca ainda fechada!\n"
                    infos = {
                        'msg': string,
                        'vez': VEZ
                    }
                    envia_mensagem(str(infos), conn)
                continue

            for conn in CONEXOES_ATIVAS:
                string = imprime_status(TABULEIRO, PLACAR, VEZ)
                infos = {
                    'msg': string,
                    'vez': VEZ
                }
                envia_mensagem(str(infos), conn)

            break
        while True:
            jogada = recebe_mensagem(CONEXOES_ATIVAS[VEZ])
            coordenadas = le_coordenada(DIM, jogada)
            i_2, j_2 = coordenadas

            if abre_peca(TABULEIRO, i_2, j_2) is False:
                for conn in CONEXOES_ATIVAS:
                    string = imprime_status(TABULEIRO, PLACAR, VEZ)
                    string += "\nEscolha uma peca ainda fechada!\n"
                    infos = {
                        'msg': string,
                        'vez': VEZ
                    }
                    envia_mensagem(str(infos), conn)
                continue

            break

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

    for conn in CONEXOES_ATIVAS:
        string = imprime_status(TABULEIRO, PLACAR, VEZ)
        remove = -len(f"Vez do Jogador {VEZ + 1}.\n")
        string = string[:remove]
        string += imprime_vencedor(PLACAR, N_JOGADORES)
        infos = {
            'msg': string,
            'vez': -1
        }
        envia_mensagem(str(infos), conn)

    for conn in CONEXOES_ATIVAS:
        try:
            envia_mensagem(b'ping', conn)
        except:
            conn.close()
            print(f'[DESCONEXÃO] {CONEXOES_ATIVAS.index(conn)} desconectado...\n')

    print(f'[FIM] Fim do jogo, reinicie o servidor...')
    server.close()


limpa_tela()
print('[LIGADO] Servidor iniciando...\n')
iniciar()
