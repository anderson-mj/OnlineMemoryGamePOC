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
import time
import sys
import random
from termcolor import colored

DIM = 4
N_JOGADORES = 2
TOTAL_DE_PARES = DIM**2 / 2
HEADER = 64
FORMAT = 'utf-8'
MENSAGEM_DESCONECTADO = '!DISC'
SERVER = '25.0.115.12'
PORT = 5050
ADDR = (SERVER, PORT)

"""
Funções de 'Server'
"""


def envia_mensagem(msg, conn):
    """
    Envia mensagens para a conexão passada
    """
    mensagem = msg.encode(FORMAT)
    envio_tam = str(len(mensagem)).encode(FORMAT)
    envio_tam += b' ' * (HEADER - len(envio_tam))
    print(f'envio_tam: {envio_tam}')
    conn.send(envio_tam)
    time.sleep(1)
    print(f'mensagem: {mensagem}')
    conn.send(mensagem)


def recebe_mensagem(conn) -> tuple[str, bool]:
    """
    Recebe mensagens da conexão passada, e indica se a conexão deve continuar ativa
    """

    KEEP_ALIVE = True
    tam_mensagem = conn.recv(HEADER).decode(FORMAT)
    if tam_mensagem:
        tam_mensagem = int(tam_mensagem)
        mensagem = conn.recv(tam_mensagem).decode(FORMAT)

    return mensagem, KEEP_ALIVE


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


def imprime_vencedor(placar, N_JOGADORES):
    """
    A partir do placar define o(s) vencedor(es) e imprime na tela
    """

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


def imprime_aguardando(aguardando):
    """
    Indica que os jogadores ainda não estão conectados
    """

    if aguardando:
        print("\n\n*** Aguardando conexões... ***\n")
        # print(colored("\n\n*** Aguardando conexões... ***\n",
        #       'red', attrs=['bold']))
        return

    # print(colored("\n*** Todos os jogadores conectados! ***",
    #       'green', attrs=['bold']))
    print("\n*** Todos os jogadores conectados! ***")

def imprime_jogador(NUMERO_JOGADOR):
    """
    Indica que um jogador se conectou
    """
    # print(f'*** Você é o jogador: ', end="")
    # print(colored(f'{NUMERO_JOGADOR}', 'cyan', attrs=['bold']), end="")
    # print(' ***')
    print(f'*** Você é o jogador: {NUMERO_JOGADOR} ***')


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
