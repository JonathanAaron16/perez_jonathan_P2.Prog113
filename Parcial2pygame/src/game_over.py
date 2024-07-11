import pygame
import sys

from funciones.configg import *
from funciones.funciones import terminar

def game_over_screen(screen, score):
    clock = pygame.time.Clock()
    running = True
    imagen_fondo = pygame.transform.scale(pygame.image.load("./src/assets/img/fondo.png"), SCREEN_SIZE)
    # Guardar el puntaje en el archivo
    name = input("Enter your initials: ")
    with open('scores.csv', 'a') as file:
        file.write(f'{name} {score}\n')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False
                from main import main_menu
                main_menu()

        screen.blit(imagen_fondo, (0,0))
        font = pygame.font.Font(None, 74)
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        prompt_text = font.render('Press Enter', True, (0, 0, 0))

        screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 300))
        screen.blit(prompt_text, (screen.get_width() // 2 - prompt_text.get_width() // 2, 400))

        pygame.display.flip()
        clock.tick(60)
