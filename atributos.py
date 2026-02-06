import random
from potencial import Jugador as JugadorCompleto
# Listas para la generación de identidad
NOMBRES = ["Lucas", "Mateo", "Julián", "Enzo", "Bautista", "Diego", "Lionel", "Lautaro", "Facundo", "Tomás"]
APELLIDOS = ["García", "Rodríguez", "Martínez", "Álvarez", "Fernández", "Romero", "Simeone", "Paredes", "Scaloni", "Gago"]

# Definición de la importancia de atributos por posición
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

def generar_nombre_aleatorio():
    """Genera una combinación aleatoria de nombre y apellido"""
    return f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"

def generar_stats_jugador(posicion):
    """
    Genera el diccionario de atributos (1-20) basado en la posición,
    respetando pesos clave y secundarios.
    """
    if posicion not in CONFIG_POSICIONES:
        return None

    stats = {}
    config = CONFIG_POSICIONES[posicion]

    for attr in TODOS_LOS_ATRIBUTOS:
        if attr in config["clave"]:
            # Atributos estrella: muy altos (14-20)
            stats[attr] = random.randint(14, 20)
        elif attr in config["secundarios"]:
            # Atributos importantes: nivel medio-alto (10-16)
            stats[attr] = random.randint(10, 16)
        else:
            # Atributos no específicos: rango bajo-medio (5-14)
            stats[attr] = random.randint(5, 14)
            
    return stats

def generar_jugador_completo(posicion, nombre=None):
    """
    Orquestador que devuelve el paquete completo de datos para 
    instanciar luego la clase Jugador en potencial.py
    """
    if nombre is None:
        nombre = generar_nombre_aleatorio()
    
    stats = generar_stats_jugador(posicion)
    
    if stats is None:
        return "Posición no válida"

    return {
        "nombre": nombre,
        "posicion": posicion,
        "atributos": stats
    }

def crear_jugadores_libres(cantidad=10):
    """Genera una lista de objetos Jugador que no pertenecen a ningún equipo."""
    libres = []
    posiciones = ["Delantero", "Defensa", "Mediocentro"]
    
    for _ in range(cantidad):
        nombre = generar_nombre_aleatorio()
        pos = random.choice(posiciones)
        edad = random.randint(18, 33)
        stats = generar_stats_jugador(pos)
        
        # Creamos la instancia del jugador
        nuevo_jugador = JugadorCompleto(nombre, pos, edad, stats)
        libres.append(nuevo_jugador)
        
    return libres   

