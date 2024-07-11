
from funciones.funciones import cargar_imagenes,cargar_rutas_imagenes_json,rotar_imagen,reescalar_imagenes


# cargar las imganes desde un Archivo JSON
rutas_imagenes = cargar_rutas_imagenes_json('sprites_imagenes.json')

#personaje
personaje_quieto = cargar_imagenes(rutas_imagenes['personaje_quieto'])
personaje_camina_derecha = cargar_imagenes(rutas_imagenes['personaje_camina_derecha'])

                            
personaje_camina_izquierda = rotar_imagen(personaje_camina_derecha)

diccionario_animaciones = {
    "Quieto": personaje_quieto,
    "Derecha": personaje_camina_derecha,
    "Izquierda": personaje_camina_izquierda
}

reescalar_imagenes(diccionario_animaciones, 80, 80)


# enemigos
enemigo_camina = cargar_imagenes(rutas_imagenes['enemigo_camina'])
enemigo_camina_izquierda = rotar_imagen(enemigo_camina)

diccionario_animaciones_enemigo = {
    "Izquierda": enemigo_camina_izquierda,
    "Derecha": enemigo_camina
}
reescalar_imagenes(diccionario_animaciones_enemigo, 60, 60)

