import random
from potencial import Jugador as JugadorCompleto

# Definición de la importancia de atributos por posición
CONFIG_POSICIONES = {
    "Portero": {
        "clave": ["Reflejos", "Agilidad", "Posicionamiento"],
        "secundarios": ["Pase", "Anticipación", "Fuerza"]
    },
    "Defensa": {
        "clave": ["Entrada", "Posicionamiento", "Fuerza"],
        "secundarios": ["Anticipación", "Resistencia", "Pase"]
    },
    "Mediocentro": {
        "clave": ["Pase", "Visión", "Control"],
        "secundarios": ["Resistencia", "Determinación", "Anticipación"]
    },
    "Delantero": {
        "clave": ["Remate", "Anticipación", "Velocidad"],
        "secundarios": ["Regate", "Control", "Determinación"]
    }
}

TODOS_LOS_ATRIBUTOS = [
    "Remate", "Pase", "Regate", "Entrada", "Control", 
    "Visión", "Posicionamiento", "Anticipación", 
    "Determinación", "Velocidad", "Resistencia", "Fuerza",
    "Reflejos", "Agilidad"
]

class Entrenador:
    def __init__(self, nombre, estilo, nivel, salario):
        self.nombre = nombre
        self.estilo = estilo  # "Ofensivo", "Defensivo", "Equilibrado"
        self.nivel = nivel    # De 1.0 a 1.5 (Multiplicador de rendimiento)
        self.salario = salario

def generar_stats_jugador(posicion):
    """
    Genera el diccionario de atributos (1-20) basado en la posición,
    respetando pesos clave y secundarios.
    """
    if posicion not in CONFIG_POSICIONES:
        return {attr: random.randint(5, 12) for attr in TODOS_LOS_ATRIBUTOS}

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
            # Atributos no específicos: rango bajo-medio (5-12)
            stats[attr] = random.randint(5, 12)
            
    return stats

def aplicar_atributos_a_jugador(nombre, posicion, edad):
    """
    Función puente para crear la instancia de JugadorCompleto 
    con stats generados dinámicamente.
    """
    stats = generar_stats_jugador(posicion)
    return JugadorCompleto(nombre, posicion, edad, stats)

def generar_candidatos_dt(cantidad=3):
    """Genera entrenadores con nombres base para que el usuario elija."""
    nombres_base = ["Ancelotti", "Guardiola", "Mourinho", "Klopp", "Simeone", "Zidane"]
    estilos = ["Ofensivo", "Defensivo", "Equilibrado"]
    candidatos = []
    
    for _ in range(cantidad):
        nombre = f"Sr. {random.choice(nombres_base)}"
        estilo = random.choice(estilos)
        nivel = round(random.uniform(1.0, 1.4), 2)
        salario = int(nivel * 200) 
        candidatos.append(Entrenador(nombre, estilo, nivel, salario))
    return candidatos