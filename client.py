"""
--- Cliente ---

Este código implementará a instância do cliente da aplicação
"""

import socket
from utils import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(ADDR)

"""
Checa se todos os jogadores estão conectados
"""
# can_play = False
# while not can_play:
#     pass

while True:
    mensagem = input('Digite uma mensagem: ')
    try:
        send_message(mensagem, server)
    except:
        server.close()
        print('Conexão encerrada')
        break

    connected = receive_message(server)
