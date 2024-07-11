import pygame
import sys
from game import * 
from funciones.configg import *
from ranking import show_ranking
from game_over import game_over_screen


# Inicializar Pygame
pygame.init()


imagen_inicio = pygame.transform.scale(pygame.image.load("./src/assets/img/titulo.png"), SCREEN_SIZE)
imagen_inicio_dos = pygame.transform.scale(pygame.image.load("./src/assets/img/fondo3.png"), SCREEN_SIZE)

# Fuente
font = pygame.font.Font(None, 74)

def main_menu():  

    while True:
        screen.blit(imagen_inicio_dos,(0,0))
        screen.blit(imagen_inicio,(0,0))    

        mouse_over_button = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()

        if draw_button(screen,font,"Play", pygame.Rect(300, 350, 200, 50), BLUE, YELLOW, game_loop):
            mouse_over_button = True
        if draw_button(screen,font,"Ranking", pygame.Rect(300, 425, 200, 50), BLUE, YELLOW, show_ranking):
            mouse_over_button = True          
        if draw_button(screen,font,"Salir", pygame.Rect(300, 500, 200, 50), RED, YELLOW, terminar):
            mouse_over_button = True

        if mouse_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()
if __name__ == '__main__':
    main_menu()
