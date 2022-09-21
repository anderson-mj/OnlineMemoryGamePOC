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
            if "\nEscolha uma peca ainda fechada!" in infos['msg'] and int(infos['vez'] + 1) != int(NUMERO_JOGADOR):
                recorte = -len("\nEscolha uma peca ainda fechada!")
                msg = infos['msg'][:recorte]
                print(msg)
                continue
            print(infos['msg'])
            if "\nPecas nao casam!\n" in infos['msg'] or "\nPecas casam!" in infos['msg'] :
                time.sleep(3)
                continue
            if int(infos['vez'] + 1) == int(NUMERO_JOGADOR):
                while True:
                    jogada = input("Especifique uma peça para virar: ")
                    try:
                        pos_i = int(jogada.split(' ')[0])
                        pos_j = int(jogada.split(' ')[1])
                    except ValueError:
                        print(
                            "Coordenadas invalidas! Use o formato \"i j\" (sem aspas),")
                        print(
                            f"onde i e j sao inteiros maiores ou iguais a 0 e menores que {DIM}")
                        continue

                    if pos_i < 0 or pos_i >= DIM:

                        print(
                            f"Coordenada i deve ser maior ou igual a zero e menor que {DIM}")
                        continue

                    if pos_j < 0 or pos_j >= DIM:
                        print(
                            f"Coordenada j deve ser maior ou igual a zero e menor que {DIM}")
                        continue
                    break
                envia_mensagem(jogada, server)
                continue
        except:
            server.close()
            print('Conexão encerrada')
            break
