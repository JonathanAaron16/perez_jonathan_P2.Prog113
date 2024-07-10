import pygame
import sys
from funciones.funciones import *
from funciones.configg import *

# Configurar la pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('kirby attack')


def game_loop():

   
    NEWEVENTENEMY = pygame.USEREVENT + 1    
    clock = pygame.time.Clock()
   
    pygame.time.set_timer(NEWEVENTENEMY, 2000)

    # cargo imagenes
    Personaje_img = pygame.image.load("./src/assets/img/Kirbyyy.png")
    imagen_fondo = pygame.transform.scale(pygame.image.load("./src/assets/img/fondo_nivel.png"), SCREEN_SIZE)


    laser_img = pygame.image.load(r"src\assets\img\kirbydisparo.png")
    laser_img = pygame.transform.scale(laser_img, (laser_width, laser_height))
    # cargo sonidos
    disparo_sonido = pygame.mixer.Sound(r"src\assets\sound\Wave6.wav")

    # cargo musica
    pygame.mixer.music.load(r"./src/assets/music/music.mp3")
    pygame.mixer.music.set_volume(0.2)

    # creo el player
    personaje = crear_personaje(diccionario_animaciones)
    #creo enemigo
    Enemigos = []
    enemigo = crear_enemigo(diccionario_animaciones_enemigo)
    # Fuente
    fuente = pygame.font.Font(None, 74)

    pygame.mixer.music.play() 
    playing_music = True
    flag_mute = False
    lasers = []
    lives = 3
    score = 0
    direcion_laser = "right"

    move_left = False
    move_right = False
    is_jumping = False
    vel_y = 0
    jump_speed = 20


    running = True
    while running:
        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_f:
                    if len(lasers) == 0:
                        laser = create_laser(personaje["rect"].midright,laser_img)
                        laser["dire_laser"] = direcion_laser
                        lasers.append(laser)
                        disparo_sonido.play()
 
                if evento.key == pygame.K_LEFT :
                    direcion_laser= "left"
                    move_left = True
                    move_right = False
                    
                if evento.key == pygame.K_RIGHT :
                    direcion_laser = "right"
                    move_right = True
                    move_left = False
                if evento.key == pygame.K_UP and not is_jumping:
                    is_jumping = True
                    vel_y = -jump_speed
                    
                if evento.key == pygame.K_m:
                    if playing_music:
                        pygame.mixer.music.pause()
                        flag_mute = True
                    else :
                        pygame.mixer.music.unpause()
                        flag_mute = False 
                    playing_music = not playing_music # o False

            # evento liberacion tecla
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT :
                    move_left = False
                if evento.key == pygame.K_RIGHT :               
                    move_right = False

            if evento.type == NEWEVENTENEMY :
                enemigo1 = crear_enemigo(diccionario_animaciones_enemigo,direccion="Derecha")
                enemigo1["rect"].topleft = (0, 350)

                enemigo = crear_enemigo(diccionario_animaciones_enemigo,direccion="Izquierda")
                enemigo["rect"].topright = (WIDTH, 350)

                Enemigos.append(enemigo)
                Enemigos.append(enemigo1)

        # Lógica del juego aquí
        is_jumping, vel_y = actualizar_salto(personaje,is_jumping,vel_y)
    
    
        for laser in lasers:
            if laser["dire_laser"] == "right":
                laser["rect"].move_ip(laser["speed"],0)
                if laser["rect"].right > WIDTH :
                    lasers.remove(laser)
            else:
                if laser["dire_laser"] == "left":
                    laser["rect"].move_ip(-laser["speed"],0)
                    if laser["rect"].left < 0 :
                        lasers.remove(laser)

        # dibujar pantalla

        actualizar_personaje(personaje,move_left,move_right)
        
        
        screen.blit(imagen_fondo, (0,0))
        
        
        screen.blit(personaje["img"], personaje["rect"])
        
        for enemy in Enemigos[:]:
            actualizar_enemigo(enemy)
            screen.blit(enemy["img"], enemy["rect"])
            
            if enemy["rect"].left < 0:
                Enemigos.remove(enemy) 


        for enemy in Enemigos[:] :
            if lasers:
                if detectar_colision_circulo(laser["rect"], enemy["rect"]):
                    Enemigos.remove(enemy)
                    score += 1
                    lasers.remove(laser)
                    if score ==  10:
                        lives += 1
        
        for enemy in Enemigos[:] :
            if detectar_colision_circulo(personaje["rect"], enemy["rect"]):
                Enemigos.remove(enemy)
                lives -= 1 
            
                if lives == 0:
                    running = False

        for laser in lasers:
            screen.blit(laser["img"], laser["rect"])


        mostrar_texto(screen,f"lives: {lives} ",fuente,POS_LAST_SCORE,RED)
        mostrar_texto(screen,f"Score: {score} ",fuente,POS_SCORE,BLUE)


        
        pygame.display.flip()
        clock.tick(60)

    # Llamar a la pantalla de game over
    from game_over import game_over_screen
    game_over_screen(screen, score)