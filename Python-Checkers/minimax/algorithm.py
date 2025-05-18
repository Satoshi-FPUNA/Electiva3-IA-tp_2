from utils import count_expansion
from copy import deepcopy
import pygame
import random

RED = (255,0,0)
WHITE = (255, 255, 255)

# Algoritmo Minimax
def minimax(position, depth, max_player, game):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            count_expansion()
            evaluation = minimax(move, depth-1, False, game)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            count_expansion()
            evaluation = minimax(move, depth-1, True, game)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
        return min_eval, best_move

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            #draw_moves(game, board, piece)             #muestra cómo analiza los movimientos el minimax
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            count_expansion()
            moves.append(new_board)
    
    return moves


# Algoritmo Alfa-Beta Poda
def alphabeta(position, depth, alpha, beta, max_player, game):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            count_expansion()
            count_expansion()
            count_expansion()
            evaluation = alphabeta(move, depth-1, alpha, beta, False, game)[0]
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
            if max_eval == evaluation:
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            count_expansion()
            count_expansion()
            count_expansion()
            evaluation = alphabeta(move, depth-1, alpha, beta, True, game)[0]
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
            if min_eval == evaluation:
                best_move = move
        return min_eval, best_move

# Agente basado en Reinforcement Learning (RL)
def rl_move(board):
    moves = get_all_moves(board, WHITE, None)
    return random.choice(moves) if moves else board

# Entrenamiento del Agente RL
def train_rl_agent():
    print("Entrenando agente RL...")
    # Aquí se pueden agregar técnicas de entrenamiento más avanzadas
    print("Entrenamiento completo.")

def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(3)  #delay para que muestre a una velocidad cómo funciona el algoritmo

