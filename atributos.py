import random

# 1. Definimos los "pesos" por posición
# Los atributos en 'clave' tendrán un rango de 14-20, los demás de 5-15
CONFIG_POSICIONES = {
    "Delantero": {
        "clave": ["Remate", "Anticipación", "Velocidad"],
        "secundarios": ["Regate", "Control", "Determinación"]
    },
    "Defensa": {
        "clave": ["Entrada", "Posicionamiento", "Fuerza"],
        "secundarios": ["Anticipación", "Resistencia", "Pase"]
    },
    "Mediocentro": {
        "clave": ["Pase", "Visión", "Control"],
        "secundarios": ["Resistencia", "Determinación", "Anticipación"]
    }
}

TODOS_LOS_ATRIBUTOS = [
    "Remate", "Pase", "Regate", "Entrada", "Control", 
    "Visión", "Posicionamiento", "Anticipación", 
    "Determinación", "Velocidad", "Resistencia", "Fuerza"
]

def generar_jugador(nombre, posicion):
    if posicion not in CONFIG_POSICIONES:
        return "Posición no válida"

    stats = {}
    config = CONFIG_POSICIONES[posicion]

    for attr in TODOS_LOS_ATRIBUTOS:
        if attr in config["clave"]:
            # Atributos estrella: muy altos
            stats[attr] = random.randint(14, 20)
        elif attr in config["secundarios"]:
            # Atributos importantes: nivel medio-alto
            stats[attr] = random.randint(10, 16)
        else:
            # Atributos no específicos: puro azar
            stats[attr] = random.randint(5, 14)
            
    return {
        "nombre": nombre,
        "posicion": posicion,
        "atributos": stats
    }

