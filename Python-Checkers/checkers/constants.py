import pygame
#biblioteca de Python diseñada para el desarrollo de videojuegos. 
# Es una interfaz sobre la biblioteca SDL (Simple DirectMedia Layer) que permite crear juegos y aplicaciones multimedia de manera sencilla.
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
