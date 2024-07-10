import pygame
import sys
from random import randrange,randint

from funciones.configg import *

def create_block(imagen=None, left=0, top=0, width=50, height=50):
    """
    Crea un bloque representado por un diccionario con un rectángulo y una imagen opcional.

    Args:
        imagen (pygame.Surface): La imagen que se mostrará en el bloque. Predeterminado es None.
        left (int): La coordenada x de la esquina superior izquierda del bloque. Predeterminado es 0.
        top (int): La coordenada y de la esquina superior izquierda del bloque. Predeterminado es 0.
        width (int): El ancho del bloque. Predeterminado es 50.
        height (int): La altura del bloque. Predeterminado es 50.

    Returns:
        dict: Un diccionario que contiene el rectángulo y la imagen del bloque.
    """
    return {"rect": pygame.Rect(left, top, width, height), "img": imagen}


def crear_personaje(diccionario_animaciones):
    """
    Crea un personaje con animación, posición y estado iniciales.

    Args:
        diccionario_animaciones (dict): Un diccionario de animaciones para diferentes estados.

    Returns:
        dict: Un diccionario que representa al personaje con imagen, rectángulo, animaciones, estado y cuadro de animación.
    """
    imagen_inicial = diccionario_animaciones["Quieto"][0]  # Seleccionar la primera imagen de la lista "Quieto"
    rect = imagen_inicial.get_rect(midleft=(WIDTH // 2, HEIGHT - 200))
    return {"img": imagen_inicial, "rect": rect, "animaciones": diccionario_animaciones, "estado": "Quieto", "animar": 0}


def crear_enemigo(diccionario_animaciones_enemigo, direccion="Izquierda"):
    """
    Crea un enemigo con animación, posición y estado iniciales.

    Args:
        diccionario_animaciones_enemigo (dict): Un diccionario de animaciones para diferentes estados del enemigo.
        direccion (str): La dirección inicial del enemigo ("Izquierda" o "Derecha"). Predeterminado es "Izquierda".

    Returns:
        dict: Un diccionario que representa al enemigo con imagen, rectángulo, animaciones, estado y cuadro de animación.
    """
    if direccion == "Izquierda":
        imagen_inicial = diccionario_animaciones_enemigo["Izquierda"][0]
        estado_inicial = "Izquierda"
    else:
        imagen_inicial = diccionario_animaciones_enemigo["Derecha"][0]
        estado_inicial = "Derecha"
    rect = imagen_inicial.get_rect(midleft=(WIDTH, HEIGHT))
    return {"img": imagen_inicial, "rect": rect, "animaciones": diccionario_animaciones_enemigo, "estado": estado_inicial, "animar": 0}


def create_laser(midright=(0, 0), laser_img=None):
    """
    Crea un láser con una posición especificada y una imagen opcional.

    Args:
        midright (tuple): La posición midright del láser. Predeterminado es (0, 0).
        laser_img (pygame.Surface): La imagen del láser. Predeterminado es None.

    Returns:
        dict: Un diccionario que representa al láser con rectángulo, imagen y velocidad.
    """
    rect = pygame.Rect(0, 0, laser_width, laser_height)
    rect.midright = midright
    return {"rect": rect, "img": laser_img, "speed": laser_speed}


def mostrar_texto(superficie, texto, fuente, coordenada, color=WHITE, color_fondo=None):
    """
    Muestra texto en una superficie.

    Args:
        superficie (pygame.Surface): La superficie en la que se mostrará el texto.
        texto (str): El texto que se mostrará.
        fuente (pygame.font.Font): La fuente utilizada para renderizar el texto.
        coordenada (tuple): Las coordenadas para centrar el texto.
        color (tuple): El color del texto. Predeterminado es WHITE.
        color_fondo (tuple): El color de fondo del texto. Predeterminado es None.

    Returns:
        None
    """
    sticker = fuente.render(texto, True, color, color_fondo)
    rect = sticker.get_rect()
    rect.center = coordenada
    superficie.blit(sticker, rect)


def wait_user(tecla):
    """
    Espera a que el usuario presione una tecla específica para continuar.

    Args:
        tecla (int): La tecla que se espera.

    Returns:
        None
    """
    continuar = True
    while continuar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == tecla:
                    continuar = False


def distancia_entre_puntos(pto_1: tuple[int, int], pto_2: tuple[int, int]):
    """
    Calcula la distancia entre dos puntos.

    Args:
        pto_1 (tuple): El primer punto (x, y).
        pto_2 (tuple): El segundo punto (x, y).

    Returns:
        float: La distancia entre los dos puntos.
    """
    base = pto_1[0] - pto_2[0]
    altura = pto_1[1] - pto_2[1]
    return (base ** 2 + altura ** 2) ** 0.5


def calcular_radio(rect):
    """
    Calcula el radio de un rectángulo basado en su ancho.

    Args:
        rect (pygame.Rect): El rectángulo para calcular el radio.

    Returns:
        int: El radio del rectángulo.
    """
    return rect.width // 2


def detectar_colision_circulo(rect1, rect2):
    """
    Detecta si dos círculos (representados por rectángulos) están colisionando.

    Args:
        rect1 (pygame.Rect): El primer rectángulo.
        rect2 (pygame.Rect): El segundo rectángulo.

    Returns:
        bool: True si los círculos están colisionando, False en caso contrario.
    """
    r1 = calcular_radio(rect1)
    r2 = calcular_radio(rect2)
    distancia = distancia_entre_puntos(rect1.center, rect2.center)
    return distancia <= r1 + r2


def draw_button(screen, font, text, rect, color, hover_color, action=None):
    """
    Dibuja un botón en la pantalla.

    Args:
        screen (pygame.Surface): La pantalla en la que se dibujará el botón.
        font (pygame.font.Font): La fuente utilizada para el texto del botón.
        text (str): El texto que se muestra en el botón.
        rect (pygame.Rect): El rectángulo que define la posición y el tamaño del botón.
        color (tuple): El color del botón.
        hover_color (tuple): El color del botón cuando está sobre él.
        action (function): La acción a realizar cuando se hace clic en el botón.

    Returns:
        bool: True si el botón está siendo presionado, False en caso contrario.
    """
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hovered = rect.collidepoint(mouse_pos)
    
    if hovered:
        pygame.draw.rect(screen, hover_color, rect)
        if click[0] == 1 and action:
            pygame.time.delay(200)
            action()
    else:
        pygame.draw.rect(screen, color, rect)
    
    text_surf = font.render(text, True, BLACK)
    screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2, rect.y + (rect.height - text_surf.get_height()) // 2))
    
    return hovered


def quit_game():
    """
    Termina el juego cerrando pygame y saliendo del sistema.

    Returns:
        None
    """
    pygame.quit()
    sys.exit()


JUMP_LIMIT = 345 
gravity = 1

def actualizar_personaje(personaje, move_left, move_right):
    """
    Actualiza la posición y animación del personaje en función del movimiento.

    Args:
        personaje (dict): El diccionario que representa al personaje.
        move_left (bool): Si el personaje se mueve hacia la izquierda.
        move_right (bool): Si el personaje se mueve hacia la derecha.

    Returns:
        None
    """
    global is_jumping, vel_y
    if move_left and personaje["rect"].left > 0:
        personaje["rect"].left -= SPEED
        personaje["estado"] = "Izquierda"
    elif move_right and personaje["rect"].right < WIDTH:
        personaje["rect"].right += SPEED
        personaje["estado"] = "Derecha"
    else:
        personaje["estado"] = "Quieto"
    
    animaciones = personaje["animaciones"][personaje["estado"]]
    personaje["animar"] = (personaje["animar"] + 1) % len(animaciones)
    personaje["img"] = animaciones[personaje["animar"]]


def actualizar_salto(personaje, is_jumping, vel_y):
    """
    Actualiza la posición del personaje durante un salto.

    Args:
        personaje (dict): El diccionario que representa al personaje.
        is_jumping (bool): Si el personaje está saltando.
        vel_y (int): La velocidad vertical del personaje.

    Returns:
        tuple: Un par (is_jumping, vel_y) que indica el estado de salto y la velocidad vertical actualizados.
    """
    if is_jumping:
        personaje["rect"].top += vel_y
        vel_y += gravity

        # Detener el salto en el punto fijo
        if personaje["rect"].top >= JUMP_LIMIT:
            personaje["rect"].top = JUMP_LIMIT
            is_jumping = False
            vel_y = 0  # Reiniciar la velocidad de caída
    return is_jumping, vel_y


def actualizar_enemigo(enemigo):
    """
    Actualiza la posición y animación del enemigo.

    Args:
        enemigo (dict): El diccionario que representa al enemigo.

    Returns:
        None
    """
    if enemigo["estado"] == "Izquierda":
        enemigo["rect"].left -= SPEED
    else:  # Estado "Derecha"
        enemigo["rect"].left += SPEED

    # Si el enemigo ha salido de la pantalla, volverlo a colocar al principio
    if enemigo["rect"].right < 0 or enemigo["rect"].left > WIDTH:
        enemigo["rect"].left = WIDTH

    animaciones = enemigo["animaciones"][enemigo["estado"]]
    enemigo["animar"] = (enemigo["animar"] + 1) % len(animaciones)
    enemigo["img"] = animaciones[enemigo["animar"]]


def terminar():
    """
    Termina el juego cerrando pygame y saliendo del sistema.

    Returns:
        None
    """
    pygame.quit()
    exit()


def reescalar_imagenes(diccionario_animaciones, ancho, alto):
    """
    Reescala todas las imágenes en el diccionario de animaciones a las dimensiones especificadas.

    Args:
        diccionario_animaciones (dict): Un diccionario de animaciones para diferentes estados.
        ancho (int): El nuevo ancho de las imágenes.
        alto (int): La nueva altura de las imágenes.

    Returns:
        None
    """
    for clave in diccionario_animaciones:
        for i in range(len(diccionario_animaciones[clave])):
            img = diccionario_animaciones[clave][i]
            diccionario_animaciones[clave][i] = pygame.transform.scale(img, (ancho, alto))


def rotar_imagen(imagenes):
    """
    Rota una lista de imágenes horizontalmente.

    Args:
        imagenes (list): Una lista de objetos pygame.Surface para rotar.

    Returns:
        list: Una lista de imágenes rotadas.
    """
    lista_imagenes = []
    for img in imagenes:
        imagen_rotada = pygame.transform.flip(img, True, False)
        lista_imagenes.append(imagen_rotada)
    return lista_imagenes


# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------

personaje_quieto = [pygame.image.load(r"src\assets\img\Kirbyyy.png")]
personaje_camina_derecha = [pygame.image.load(r"src\assets\img\caminar1.png"),
                            pygame.image.load(r"src\assets\img\caminar2.png"),
                            pygame.image.load(r"src\assets\img\caminar3.png"),
                            pygame.image.load(r"src\assets\img\caminar4.png"),
                            pygame.image.load(r"src\assets\img\caminar5.png")
                            ]
personaje_camina_izquierda = rotar_imagen(personaje_camina_derecha)

diccionario_animaciones = {
    "Quieto": personaje_quieto,
    "Derecha": personaje_camina_derecha,
    "Izquierda": personaje_camina_izquierda
}

reescalar_imagenes(diccionario_animaciones, 80, 80)


enemigo_camina = [
                   pygame.image.load(r"src\assets\img\enemigo1.png"),
                   pygame.image.load(r"src\assets\img\enemigo3.png"),
                   pygame.image.load(r"src\assets\img\enemigo4.png")]
enemigo_camina_izquierda = rotar_imagen(enemigo_camina)

diccionario_animaciones_enemigo = {
    "Izquierda": enemigo_camina_izquierda,
    "Derecha": enemigo_camina
}
reescalar_imagenes(diccionario_animaciones_enemigo, 60, 60)

