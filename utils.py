"""
--- Utils ---

Este código implementará um módulo de utilidades para o projeto
"""

import os
import random
import time

"""
Configurações do servidor
"""
HEADER = 64
FORMAT = 'utf-8'
MENSAGEM_DESCONECTADO = '!DISCONNECT'
SERVER = '25.0.115.12'
PORT = 5050
ADDR = (SERVER, PORT)

"""
Configurações do jogo
"""
DIM = 2
N_JOGADORES = 2
TOTAL_DE_PARES = DIM**2 / 2


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
    conn.send(envio_tam)
    conn.send(mensagem)


def recebe_mensagem(conn):
    """
    Recebe mensagens da conexão passada, e indica se a conexão deve continuar ativa
    """
    tam_mensagem = conn.recv(HEADER).decode(FORMAT)
    if tam_mensagem:
        tam_mensagem = int(tam_mensagem)
        mensagem = conn.recv(tam_mensagem).decode(FORMAT)

    return mensagem


"""
Funções de 'Front'
"""


def limpa_tela() -> None:
    """
    Limpa o terminal
    """

    os.system('cls' if os.name == 'nt' else 'clear')

def reimprime_tabuleiro(tabuleiro_atual):
    """
    Reimprime o tabuleiro no terminal com um delay
    """
    time.sleep(3)
    limpa_tela()
    print(tabuleiro_atual['msg'])


def imprime_tabuleiro(tabuleiro_atual) -> None:
    """
    Imprime o tabuleiro no terminal
    """
    string = ""
    dim = len(tabuleiro_atual)
    string+= "    "

    for k in range(0, dim):
        string += f" {k} "

    string += "\n"
    string += "-----"

    for k in range(0, dim):
        string += "---"

    string += "\n"

    for k in range(0, dim):
        string += f"{k} | "

        for j in range(0, dim):
            if tabuleiro_atual[k][j] == '-':
                string += " - "

            elif tabuleiro_atual[k][j] >= 0:
                string += f" {tabuleiro_atual[k][j]} "

            else:
                string += " ? "

        string += "\n"
    return string


def imprime_placar(placar_atual) -> None:
    """
    Imprime o placar atual
    """
    string = ""
    n_jogadores = len(placar_atual)

    string+= "Placar:\n"
    string+= "---------------------\n"
    for jogador in range(0, n_jogadores):
        string += f"Jogador {jogador + 1}: {placar_atual[jogador]}\n"

    return string


def imprime_status(tabuleiro_atual, placar_atual, vez) -> None:
    """
    Imprime o status do jogo
    """
    string = ""
    string += imprime_tabuleiro(tabuleiro_atual)
    string += '\n'

    string += imprime_placar(placar_atual)
    string += '\n'
    string += '\n'

    string += f"Vez do Jogador {vez + 1}.\n"
    return string


def imprime_vencedor(placar, N_JOGADORES):
    """
    A partir do placar define o(s) vencedor(es) e imprime na tela
    """
    string = ""
    pontuacao_maxima = max(placar)
    vencedores = []

    for i in range(0, N_JOGADORES):
        if placar[i] == pontuacao_maxima:
            vencedores.append(i)

    if len(vencedores) > 1:
        string += "Houve empate entre os jogadores "
        for i in vencedores:
            string += str(i + 1) + ' '


    else:
        string += f"Jogador {vencedores[0] + 1} foi o vencedor!"

    return string


def imprime_aguardando(aguardando):
    """
    Indica que os jogadores ainda não estão conectados
    """
    if aguardando:
        print("\n\n*** Aguardando conexões... ***\n")
        return

    print("\n*** Todos os jogadores conectados! ***")

def imprime_jogador(NUMERO_JOGADOR):
    """
    Indica que um jogador se conectou
    """
    print(f'*** Você é o jogador: {NUMERO_JOGADOR} ***')

def le_coordenada(dim, input_coordenada) -> any:
    """
    Le a coordenada que o jogador irá digitar
    """
    pos_i = int(input_coordenada.split(' ')[0])
    pos_j = int(input_coordenada.split(' ')[1])

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
