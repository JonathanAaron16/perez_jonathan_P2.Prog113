import pygame
import sys
from game import *

def show_ranking():
    clock = pygame.time.Clock()
    running = True
    imagen_fondo = pygame.transform.scale(pygame.image.load("./src/assets/img/fondo2.png"), SCREEN_SIZE)
    # Leer los scores desde un archivo
    try:
        with open('scores.csv', 'r') as file:
            scores = [line.strip().split() for line in file.readlines()]
    except FileNotFoundError:
        scores = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        

        font = pygame.font.Font(None, 36)
        y_offset = 100

        screen.blit(imagen_fondo, (0,0))

        for score in scores:
            score_text = font.render(f'{score[0]}: {score[1]}', True, RED)
            screen.blit(score_text, (100, y_offset))
            y_offset += 40

        pygame.display.flip()
        clock.tick(60)
