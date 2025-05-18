import numpy as np
import random

class RLAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.alpha = alpha  # Tasa de aprendizaje
        self.gamma = gamma  # Factor de descuento
        self.epsilon = epsilon  # Factor de exploración
        self.q_table = {}  # Tabla Q para almacenar valores estado-acción

    def get_state_key(self, board):
        """
        Convierte el tablero en una representación de cadena para usar como clave en la tabla Q.
        """
        return str(board)

    def choose_action(self, state, possible_actions):
        """
        Elige una acción usando la política epsilon-greedy.
        """
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(possible_actions)  # Exploración
        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = {action: 0.0 for action in possible_actions}
        return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def update_q_value(self, state, action, reward, next_state, possible_actions):
        """
        Actualiza el valor Q utilizando la fórmula de Q-learning.
        """
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0.0 for a in possible_actions}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {a: 0.0 for a in possible_actions}

        current_q = self.q_table[state_key][action]
        max_future_q = max(self.q_table[next_state_key].values(), default=0)

        # Actualización Q-learning
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.q_table[state_key][action] = new_q

    def train(self, state, action, reward, next_state, possible_actions):
        self.update_q_value(state, action, reward, next_state, possible_actions)

    def play_move(self, board, possible_actions):
        action = self.choose_action(board, possible_actions)
        return action

    def save_q_table(self, filename='q_table.npy'):
        np.save(filename, self.q_table)

    def load_q_table(self, filename='q_table.npy'):
        try:
            self.q_table = np.load(filename, allow_pickle=True).item()
            print("Q-table cargada correctamente.")
        except FileNotFoundError:
            print("No se encontró el archivo Q-table. Se inicializa una nueva tabla.")
