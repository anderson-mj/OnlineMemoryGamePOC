"""
messageServerClient = {
  'tabuleiro': [[]],
  'vez': 0,
  'placar': {'0': 0, '1': 0}
}

messageClientServer = {
  'peça': {'i': 0, 'j': 0},
  'vez': 0
}
"""


"""
Módulo de utilidades para o projeto
"""

"""
Constantes e funções utilizadas ao longo do projeto
"""
import socket
import os
import sys
import time
import random
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '25.0.115.12'
PORT = 5050
ADDR = (SERVER, PORT)

"""
Funções de 'Server'
"""


def send_message(msg, conn):
    """
    Envia mensagens para a conexão passada
    """
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    conn.send(send_len)
    conn.send(message)


def receive_message(conn):
    keep_alive = True
    msg_len = conn.recv(HEADER).decode(FORMAT)
    if msg_len:
        msg_len = int(msg_len)
        msg = conn.recv(msg_len).decode(FORMAT)

    if msg == DISCONNECT_MESSAGE:
        keep_alive = False

    print(f'Mensagem recebida: {msg}')
    return keep_alive


def send_dict(dict, conn):
    pass


"""
Funções de 'Front'
"""


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


"""
Funções de 'Back'
"""


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
