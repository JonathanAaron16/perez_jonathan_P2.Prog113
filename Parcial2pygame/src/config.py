import pygame
import sys

def config_menu(screen):
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.fill((255, 255, 255))

        # Dibujar elementos de configuración aquí

        pygame.display.flip()
        clock.tick(60)
