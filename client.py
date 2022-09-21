"""
--- Cliente ---

Este código implementará a instância do cliente da aplicação
"""

import socket
import time
import ast
from utils import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(ADDR)
CAN_PLAY = False

limpa_tela()

NUMERO_JOGADOR, KEEP_ALIVE = recebe_mensagem(server)
NUMERO_JOGADOR = int(NUMERO_JOGADOR)
imprime_jogador(NUMERO_JOGADOR)

while KEEP_ALIVE:
    if not CAN_PLAY:
        imprime_aguardando(True)
        mensagem, KEEP_ALIVE = recebe_mensagem(server)
        if mensagem == 'CAN_PLAY':
            CAN_PLAY = True
            imprime_aguardando(False)
            time.sleep(3)
    else:
        infos, KEEP_ALIVE = recebe_mensagem(server)
        infos = ast.literal_eval(infos)

        imprime_status(infos['tabuleiro'], infos['placar'], infos['vez'])

        if NUMERO_JOGADOR == infos['vez'] + 1:
            while infos['pares_encontrados'] < TOTAL_DE_PARES:
                while True:
                    imprime_status(infos['tabuleiro'],
                                   infos['placar'], infos['vez'])

                    coordenadas = le_coordenada(DIM)

                    if coordenadas is False:
                        continue

                    i_1, j_1 = coordenadas

                    if abre_peca(infos['tabuleiro'], i_1, j_1) is False:

                        print("Escolha uma peca ainda fechada!")
                        input("Pressione <enter> para continuar...")
                        continue

                    
                    break

                while True:
                    imprime_status(infos['tabuleiro'],
                                   infos['placar'], infos['vez'])

                    coordenadas = le_coordenada(DIM)

                    if coordenadas is False:
                        continue

                    i_2, j_2 = coordenadas

                    if abre_peca(infos['tabuleiro'], i_2, j_2) is False:

                        print("Escolha uma peca ainda fechada!")
                        input("Pressione <enter> para continuar...")
                        continue

                    
                    break

                imprime_status(infos['tabuleiro'],
                               infos['placar'], infos['vez'])

                print(
                    f"Pecas escolhidas --> ({i_1}, {j_1}) e ({i_2}, {j_2})\n")
                
                if infos['tabuleiro'][i_1][j_1] == infos['tabuleiro'][i_2][j_2]:

                    print(f"Pecas casam! Ponto para o jogador {infos['vez'] + 1}.")

                    incrementa_placar(infos['placar'], infos['vez'])
                    infos['pares_encontrados'] = infos['pares_encontrados'] + 1
                    remove_peca(infos['tabuleiro'], i_1, j_1)
                    remove_peca(infos['tabuleiro'], i_2, j_2)

                else:

                    print("Pecas nao casam!")

                    fecha_peca(infos['tabuleiro'], i_1, j_1)
                    fecha_peca(infos['tabuleiro'], i_2, j_2)
                    infos['vez'] = (infos['vez'] + 1) % N_JOGADORES
                
                envia_mensagem(str(infos), server)
                break
        else:
            print("*** Espere a sua vez ***")
