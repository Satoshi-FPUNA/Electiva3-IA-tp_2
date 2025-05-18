import pygame
import tkinter as tk
from tkinter import ttk
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax, alphabeta, rl_move
from rl.rl_agent import RLAgent
import time
FPS = 60

# Inicializar Pygame
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

# Inicializar el agente RL
rl_agent = RLAgent()

# Variables de medición
from utils import count_expansion, reset_expansion_count, get_expansion_count

time_taken = 0.0

# Totales acumulados por algoritmo
total_time = {'Minimax': 0.0, 'AlfaBeta': 0.0, 'RL': 0.0}
total_states = {'Minimax': 0, 'AlfaBeta': 0, 'RL': 0}

# Función para obtener fila y columna a partir de la posición del mouse
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Función para medir el tiempo y los nodos expandidos
def measure_performance(func, algorithm, *args):
    global time_taken
    start_time = time.time()
    reset_expansion_count()
    result = func(*args)
    time_taken = time.time() - start_time
    total_time[algorithm] += time_taken
    total_states[algorithm] += get_expansion_count()
    print(f"[{algorithm}] Tiempo de ejecución: {time_taken:.4f} segundos")
    print(f"[{algorithm}] Estados expandidos: {get_expansion_count()}")
    return result

# Función para contar estados expandidos
def count_expansion():
    global states_expanded
    states_expanded += 1

# Mostrar resultados en la interfaz
def display_performance():
    root = tk.Toplevel()
    root.title("Resultados de Rendimiento")
    for algo in total_time:
        ttk.Label(root, text=f"{algo} - Tiempo total: {total_time[algo]:.4f} segundos").pack()
        ttk.Label(root, text=f"{algo} - Estados expandidos: {total_states[algo]}").pack()
    ttk.Button(root, text="Cerrar", command=root.destroy).pack()
    root.mainloop()

# Actualizar el rendimiento al finalizar el juego
def show_performance():
    print("--- Rendimiento Acumulado ---")
    for algo in total_time:
        print(f"{algo} - Tiempo total: {total_time[algo]:.4f} segundos")
        print(f"{algo} - Estados expandidos: {total_states[algo]}")
    display_performance()

# Mostrar ventana emergente de resultado con Pygame
def show_result_pygame(message):
    font = pygame.font.SysFont('Arial', 50)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.fill((0, 0, 0))
    WIN.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

# Verificar si un jugador tiene movimientos válidos
def has_valid_moves(board, color):
    if board is None:
        return False
    for piece in board.get_all_pieces(color):
        moves = board.get_valid_moves(piece)
        if moves:
            return True
    return False

# Movimiento del agente RL
def rl_agent_move(board, game):
    try:
        possible_moves = {}  # Almacenar los movimientos válidos

        for piece in board.get_all_pieces(game.turn):
            moves = board.get_valid_moves(piece)
            for move, skip in moves.items():
                # Verificar que el movimiento esté dentro de los límites del tablero
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    possible_moves[(piece.row, piece.col, move[0], move[1])] = (piece, move, skip)

        # Verificar si hay movimientos válidos
        if not possible_moves:
            print("No hay movimientos válidos")
            return board

        # Elegir un movimiento usando el agente RL
        action = rl_agent.play_move(board, list(possible_moves.keys()))
        if action and action in possible_moves:
            piece, move, skip = possible_moves[action]
            # Validar si el movimiento realmente pertenece a los movimientos válidos del tablero
            valid_moves = board.get_valid_moves(piece)
            if move in valid_moves:
                print(f"Movimiento seleccionado: {action}")
                # Realizar el movimiento y eliminar las piezas capturadas
                board.move(piece, move[0], move[1])
                if skip:
                    # Asegurarse de que skip sea una lista de piezas a eliminar
                    if isinstance(skip, list):
                        for skipped_piece in skip:
                            board.remove([skipped_piece])
                    else:
                        board.remove([skip])
                    print("Pieza capturada eliminada del tablero.")
                return board
            else:
                print("El movimiento seleccionado no está en los movimientos válidos.")
                return board
        else:
            print("El agente RL no encontró un movimiento válido.")
            return board
    except Exception as e:
        print(f"Error en rl_agent_move: {e}")
        return board
    try:
        possible_moves = {}  # Almacenar los movimientos válidos

        for piece in board.get_all_pieces(game.turn):
            moves = board.get_valid_moves(piece)
            for move, skip in moves.items():
                # Verificar que el movimiento esté dentro de los límites del tablero
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    possible_moves[(piece.row, piece.col, move[0], move[1])] = (piece, move, skip)

        # Verificar si hay movimientos válidos
        if not possible_moves:
            print("No hay movimientos válidos para el agente RL.")
            return board

        # Elegir un movimiento usando el agente RL
        action = rl_agent.play_move(board, list(possible_moves.keys()))
        if action and action in possible_moves:
            piece, move, skip = possible_moves[action]
            # Validar si el movimiento realmente pertenece a los movimientos válidos del tablero
            valid_moves = board.get_valid_moves(piece)
            if move in valid_moves:
                print(f"Movimiento seleccionado por RL: {action}")
                # Realizar el movimiento y eliminar las piezas capturadas
                board.move(piece, move[0], move[1])
                if skip:
                    board.remove(skip)
                    print("Pieza capturada eliminada del tablero.")
                return board
            else:
                print("El movimiento seleccionado no está en los movimientos válidos.")
                return board
        else:
            print("El agente RL no encontró un movimiento válido.")
            return board
    except Exception as e:
        print(f"Error en rl_agent_move: {e}")
        return board
    try:
        possible_moves = {}  # Almacenar los movimientos válidos

        for piece in board.get_all_pieces(game.turn):
            moves = board.get_valid_moves(piece)
            for move, skip in moves.items():
                # Verificar que el movimiento esté dentro de los límites del tablero
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    possible_moves[(piece.row, piece.col, move[0], move[1])] = (piece, move)

        # Verificar si hay movimientos válidos
        if not possible_moves:
            print("No hay movimientos válidos para el agente RL.")
            return board

        # Elegir un movimiento usando el agente RL
        action = rl_agent.play_move(board, list(possible_moves.keys()))
        if action and action in possible_moves:
            piece, move = possible_moves[action]
            # Validar si el movimiento realmente pertenece a los movimientos válidos del tablero
            valid_moves = board.get_valid_moves(piece)
            if move in valid_moves:
                print(f"Movimiento seleccionado por RL: {action}")
                board.move(piece, move[0], move[1])
                return board
            else:
                print("El movimiento seleccionado no está en los movimientos válidos.")
                return board
        else:
            print("El agente RL no encontró un movimiento válido.")
            return board
    except Exception as e:
        print(f"Error en rl_agent_move: {e}")
        return board
    try:
        possible_moves = {}  # Almacenar los movimientos válidos

        for piece in board.get_all_pieces(game.turn):
            moves = board.get_valid_moves(piece)
            for move, skip in moves.items():
                # Verificar que el movimiento esté dentro de los límites del tablero
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    possible_moves[(piece.row, piece.col, move[0], move[1])] = (piece, move)

        # Verificar si hay movimientos válidos
        if not possible_moves:
            print("No hay movimientos válidos para el agente RL.")
            return board

        # Elegir un movimiento usando el agente RL
        action = rl_agent.play_move(board, list(possible_moves.keys()))
        if action:
            piece, move = possible_moves.get(action, (None, None))
            if piece and move:
                print(f"Movimiento seleccionado por RL: {action}")
                board.move(piece, move[0], move[1])
                return board
            else:
                print("El movimiento seleccionado no es válido.")
                return board
        else:
            print("El agente RL no encontró un movimiento válido.")
            return board
    except Exception as e:
        print(f"Error en rl_agent_move: {e}")
        return board
    try:
        possible_moves = {}  # Almacenar los movimientos válidos

        for piece in board.get_all_pieces(game.turn):
            moves = board.get_valid_moves(piece)
            for move, skip in moves.items():
                possible_moves[(piece.row, piece.col, move[0], move[1])] = (piece, move)

        # Verificar si hay movimientos válidos
        if not possible_moves:
            print("No hay movimientos válidos para el agente RL.")
            return board

        # Elegir un movimiento usando el agente RL
        action = rl_agent.play_move(board, list(possible_moves.keys()))
        if action:
            piece, move = possible_moves[action]
            print(f"Movimiento seleccionado por RL: {action}")
            board.move(piece, move[0], move[1])
            return board
        else:
            print("El agente RL no encontró un movimiento válido.")
            return board
    except Exception as e:
        print(f"Error en rl_agent_move: {e}")
        return board

# Función principal del juego
def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False    
        clock.tick(FPS)
        try:
            # Verificar empate: si el jugador actual no tiene movimientos válidos
            if not has_valid_moves(game.get_board(), game.turn):
                print("Empate: Sin movimientos disponibles.")
                show_result_pygame("Empate: Sin movimientos disponibles")
                show_performance()
                run = False

            # Verificar si el turno es de un humano
            if (game.turn == WHITE and player1_algorithm == 'Humano') or (game.turn == RED and player2_algorithm == 'Humano'):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        game.select(row, col)
                game.update()
                continue

            # Turno de la IA
            if game.turn == WHITE:
                if player1_algorithm == 'Minimax':
                    value, new_board = measure_performance(minimax, 'Minimax', game.get_board(), player1_depth, True, game)
                    game.ai_move(new_board)
                elif player1_algorithm == 'AlfaBeta':
                    value, new_board = measure_performance(alphabeta, 'AlfaBeta', game.get_board(), player1_depth, float('-inf'), float('inf'), True, game)
                    game.ai_move(new_board)
                elif player1_algorithm == 'RL':
                    new_board = measure_performance(rl_agent_move, 'RL', game.get_board(), game)
                    game.ai_move(new_board)
            else:
                if player2_algorithm == 'Minimax':
                    value, new_board = measure_performance(minimax, 'Minimax', game.get_board(), player2_depth, False, game)
                    game.ai_move(new_board)
                elif player2_algorithm == 'AlfaBeta':
                    value, new_board = measure_performance(alphabeta, 'AlfaBeta', game.get_board(), player2_depth, float('-inf'), float('inf'), False, game)
                    game.ai_move(new_board)
                elif player2_algorithm == 'RL':
                    new_board = measure_performance(rl_agent_move, 'RL', game.get_board(), game)
                    game.ai_move(new_board)

            if game.get_board() and game.winner() is not None:
                show_performance()
                winner = game.winner()
                print(f'Ganador: {winner}')
                message = 'Ganador: Blanco' if winner == WHITE else 'Ganador: Rojo'
                show_result_pygame(message)
                run = False

        except Exception as e:
            print(f'Error durante el turno: {e}')
            run = False

        game.update()

    pygame.quit()
    print("Juego finalizado correctamente.")
# Función para iniciar el juego con la configuración seleccionada
def start_game():
    global player1_algorithm, player2_algorithm, player1_depth, player2_depth
    player1_algorithm = player1_algo_var.get()
    player2_algorithm = player2_algo_var.get()
    player1_depth = int(player1_depth_var.get())
    player2_depth = int(player2_depth_var.get())
    root.destroy()
    main()

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Configuración de Juego de Damas")

label_player1 = ttk.Label(root, text="Jugador 1 (Blancas) - Algoritmo:")
label_player1.pack()
player1_algo_var = tk.StringVar(value='Minimax')
combo_player1_algo = ttk.Combobox(root, textvariable=player1_algo_var, values=['Humano', 'Minimax', 'AlfaBeta', 'RL'])
combo_player1_algo.pack()

label_player1_depth = ttk.Label(root, text="Profundidad Jugador 1 (1-5):")
label_player1_depth.pack()
player1_depth_var = tk.IntVar(value=3)
combo_player1_depth = ttk.Combobox(root, textvariable=player1_depth_var, values=[1, 2, 3, 4, 5])
combo_player1_depth.pack()

label_player2 = ttk.Label(root, text="Jugador 2 (Rojas) - Algoritmo:")
label_player2.pack()
player2_algo_var = tk.StringVar(value='RL')
combo_player2_algo = ttk.Combobox(root, textvariable=player2_algo_var, values=['Humano', 'Minimax', 'AlfaBeta', 'RL'])
combo_player2_algo.pack()

label_player2_depth = ttk.Label(root, text="Profundidad Jugador 2 (1-5):")
label_player2_depth.pack()
player2_depth_var = tk.IntVar(value=3)
combo_player2_depth = ttk.Combobox(root, textvariable=player2_depth_var, values=[1, 2, 3, 4, 5])
combo_player2_depth.pack()

button_start = ttk.Button(root, text="Iniciar Juego", command=start_game)
button_start.pack(pady=10)

root.mainloop()

if __name__ == '__main__':
    main()
