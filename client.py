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
        limpa_tela()
        infos, KEEP_ALIVE = recebe_mensagem(server)
        infos = ast.literal_eval(infos)
        
        imprime_status(infos['tabuleiro'], infos['placar'], infos['vez'])

        mensagem = input('Digite uma mensagem: ')