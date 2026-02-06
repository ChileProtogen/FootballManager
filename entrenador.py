import random
from atributos import generar_nombre_aleatorio as generar_nombre

class Entrenador:
    def __init__(self, nombre, estilo, nivel, salario):
        self.nombre = nombre
        self.estilo = estilo # "Ofensivo", "Defensivo", "Equilibrado"
        self.nivel = nivel   # 1 a 10 (afecta la progresión de los jugadores)
        self.salario = salario # Coste por jornada