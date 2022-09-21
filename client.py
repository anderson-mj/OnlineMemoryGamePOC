"""
--- Cliente ---

Este código implementará a instância do cliente da aplicação
"""

import socket
from utils import *
import time
import ast

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
        try:
            msg, KEEP_ALIVE = recebe_mensagem(server)
            limpa_tela()
            infos = ast.literal_eval(msg)
            print(infos['msg'])
            if "\nPecas nao casam!\n" in infos['msg'] or "\nPecas casam!" in infos['msg']:
                time.sleep(3)
                continue
            if int(infos['vez'] + 1) == int(NUMERO_JOGADOR):
                jogada = input("Especifique uma peça para virar: ")
                envia_mensagem(jogada, server)
                continue
        except:
            server.close()
            print('Conexão encerrada')
            break
