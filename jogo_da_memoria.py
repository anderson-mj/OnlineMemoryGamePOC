"""Jogo da memória

Este código implementa um jogo da memória que será jogado entre dois jogadores
através de uma conexão por sockets.
"""

import os
import sys
import time
import random


def limpa_tela() -> None:
    """
    Limpa o terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def imprime_tabuleiro(tabuleiro_atual) -> None:
    """
    Imprime o tabuleiro no terminal
    """

    limpa_tela()

    dim = len(tabuleiro_atual)
    sys.stdout.write("    ")

    for k in range(0, dim):
        sys.stdout.write(f" {k} ")

    sys.stdout.write("\n")
    sys.stdout.write("-----")

    for k in range(0, dim):
        sys.stdout.write("---")

    sys.stdout.write("\n")

    for k in range(0, dim):
        sys.stdout.write(f"{k} | ")

        for j in range(0, dim):
            if tabuleiro_atual[k][j] == '-':
                sys.stdout.write(" - ")

            elif tabuleiro_atual[k][j] >= 0:
                sys.stdout.write(f" {tabuleiro_atual[k][j]} ")

            else:
                sys.stdout.write(" ? ")

        sys.stdout.write("\n")


def novo_tabuleiro(dim) -> list:
    """
    Cria um novo tabuleiro para a partida
    """

    tabuleiro_novo = []
    posicoes_disponiveis = []

    for _ in range(0, dim):
        linha = []
        for j in range(0, dim):
            linha.append(0)

        tabuleiro_novo.append(linha)

    for k in range(0, dim):
        for j in range(0, dim):
            posicoes_disponiveis.append((k, j))

    for j in range(0, dim // 2):
        for k in range(1, dim + 1):
            maximo = len(posicoes_disponiveis)
            indice_aleatorio = random.randint(0, maximo - 1)
            r_i, r_j = posicoes_disponiveis.pop(indice_aleatorio)

            tabuleiro_novo[r_i][r_j] = -k

            maximo = len(posicoes_disponiveis)
            indice_aleatorio = random.randint(0, maximo - 1)
            r_i, r_j = posicoes_disponiveis.pop(indice_aleatorio)

            tabuleiro_novo[r_i][r_j] = -k

    return tabuleiro_novo


def abre_peca(tabuleiro_atual, pos_i, pos_j) -> bool:
    """
    Abre a peça escolhida pelo jogador
    """
    if tabuleiro_atual[pos_i][pos_j] == '-':
        return False
    if tabuleiro_atual[pos_i][pos_j] < 0:
        tabuleiro_atual[pos_i][pos_j] = -tabuleiro_atual[pos_i][pos_j]
        return True

    return False


def fecha_peca(tabuleiro_atual, pos_i, pos_j) -> bool:
    """
    Fecha a peça escolhida pelo jogador
    """

    if tabuleiro_atual[pos_i][pos_j] == '-':
        return False
    if tabuleiro_atual[pos_i][pos_j] > 0:
        tabuleiro_atual[pos_i][pos_j] = -tabuleiro_atual[pos_i][pos_j]
        return True

    return False


def remove_peca(tabuleiro_atual, pos_i, pos_j) -> bool:
    """
    Remove a peça escolhida pelo jogador
    """

    if tabuleiro_atual[pos_i][pos_j] == '-':
        return False

    tabuleiro_atual[pos_i][pos_j] = "-"
    return True


def novo_placar(n_jogadores) -> list:
    """
    Cria um novo placar
    """

    return [0] * n_jogadores


def incrementa_placar(placar_atual, jogador) -> None:
    """
    Incrementa o placar pra um jogador
    """

    placar_atual[jogador] = placar_atual[jogador] + 1


def imprime_placar(placar_atual) -> None:
    """
    Imprime o placar atual
    """

    n_jogadores = len(placar_atual)

    print("Placar:")
    print("---------------------")
    for jogador in range(0, n_jogadores):
        print(f"Jogador {jogador + 1}: {placar_atual[jogador]}")


def imprime_status(tabuleiro_atual, placar_atual, vez) -> None:
    """
    Imprime o status do jogo
    """

    imprime_tabuleiro(tabuleiro_atual)
    sys.stdout.write('\n')

    imprime_placar(placar_atual)
    sys.stdout.write('\n')
    sys.stdout.write('\n')

    print(f"Vez do Jogador {vez + 1}.\n")


def le_coordenada(dim) -> any:
    """
    Le a coordenada que o jogador irá digitar
    """

    input_coordenada = input("Especifique uma peca: ")

    try:
        pos_i = int(input_coordenada.split(' ')[0])
        pos_j = int(input_coordenada.split(' ')[1])
    except ValueError:
        print(
            "Coordenadas invalidas! Use o formato \"i j\" (sem aspas),")
        print(
            f"onde i e j sao inteiros maiores ou iguais a 0 e menores que {dim}")
        input("Pressione <enter> para continuar...")
        return False

    if pos_i < 0 or pos_i >= dim:

        print(
            f"Coordenada i deve ser maior ou igual a zero e menor que {dim}")
        input("Pressione <enter> para continuar...")
        return False

    if pos_j < 0 or pos_j >= dim:

        print(
            f"Coordenada j deve ser maior ou igual a zero e menor que {dim}")
        input("Pressione <enter> para continuar...")
        return False

    return (pos_i, pos_j)


DIM = 4

N_JOGADORES = 2

TOTAL_DE_PARES = DIM**2 / 2

PARES_ENCONTRADOS = 0

VEZ = 0

tabuleiro = novo_tabuleiro(DIM)

placar = novo_placar(N_JOGADORES)

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

        time.sleep(5)
    else:

        print("Pecas nao casam!")

        time.sleep(3)

        fecha_peca(tabuleiro, i_1, j_1)
        fecha_peca(tabuleiro, i_2, j_2)
        VEZ = (VEZ + 1) % N_JOGADORES

pontuacao_maxima = max(placar)
vencedores = []

for i in range(0, N_JOGADORES):
    if placar[i] == pontuacao_maxima:
        vencedores.append(i)

if len(vencedores) > 1:
    sys.stdout.write("Houve empate entre os jogadores ")
    for i in vencedores:
        sys.stdout.write(str(i + 1) + ' ')

    sys.stdout.write("\n")

else:
    print(f"Jogador {vencedores[0] + 1} foi o vencedor!")
