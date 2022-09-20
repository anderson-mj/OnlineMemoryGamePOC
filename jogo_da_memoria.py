"""Jogo da memória

Este código implementa um jogo da memória que será jogado entre dois jogadores
através de uma conexão por sockets.
"""

import sys # FOI
import time # FOI
from utils import * # FOI

DIM = 4 # FOI

N_JOGADORES = 2 # FOI

TOTAL_DE_PARES = DIM**2 / 2 # FOI

PARES_ENCONTRADOS = 0 # FOI

VEZ = 0 # FOI

tabuleiro = novo_tabuleiro(DIM) # FOI

placar = novo_placar(N_JOGADORES) # FOI

while PARES_ENCONTRADOS < TOTAL_DE_PARES:
    while True:
        imprime_status(tabuleiro, placar, VEZ)

        coordenadas = le_coordenada(DIM)
        if coordenadas is False:
            continue

        i_1, j_1 = coordenadas

        if abre_peca(tabuleiro, i_1, j_1) is False:
            print("Escolha uma peca ainda fechada!")
            input("Pressione <enter> para continuar...")
            continue

        break

    while True:
        imprime_status(tabuleiro, placar, VEZ)

        coordenadas = le_coordenada(DIM)
        if coordenadas is False:
            continue

        i_2, j_2 = coordenadas

        if abre_peca(tabuleiro, i_2, j_2) is False:

            print("Escolha uma peca ainda fechada!")
            input("Pressione <enter> para continuar...")
            continue

        break

    imprime_status(tabuleiro, placar, VEZ)

    print(
        f"Pecas escolhidas --> ({i_1}, {j_1}) e ({i_2}, {j_2})\n")

    if tabuleiro[i_1][j_1] == tabuleiro[i_2][j_2]:

        print(f"Pecas casam! Ponto para o jogador {VEZ + 1}.")

        incrementa_placar(placar, VEZ)
        PARES_ENCONTRADOS = PARES_ENCONTRADOS + 1
        remove_peca(tabuleiro, i_1, j_1)
        remove_peca(tabuleiro, i_2, j_2)

        # MANDA MENSAGEM PARA O SERVIDOR
        time.sleep(5)
    else:

        print("Pecas nao casam!")

        time.sleep(3)

        fecha_peca(tabuleiro, i_1, j_1)
        fecha_peca(tabuleiro, i_2, j_2)
        VEZ = (VEZ + 1) % N_JOGADORES

    imprime_vencedor(placar, N_JOGADORES)
