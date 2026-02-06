import random

class Jugador:
    def __init__(self, nombre, posicion, edad):
        self.nombre = nombre
        self.posicion = posicion
        self.edad = edad
        
        # Potencial: 0 a 200 (Al estilo FM)
        # Un 'Wonderkid' tendría 170+, un jugador normal 110
        self.pa = random.randint(100, 200) 
        self.ca = random.randint(80, self.pa - 10) # Empieza por debajo de su potencial
        
        self.atributos = self._generar_atributos_base()

    def _generar_atributos_base(self):
        # Escala los atributos (1-20) basados en su CA actual
        # Un CA de 100 daría una media de atributos de ~10
        base = self.ca / 10
        stats = {}
        
        atributos_lista = ["Remate", "Pase", "Entrada", "Velocidad", "Vision"]
        
        for attr in atributos_lista:
            # Añadimos un pequeño factor aleatorio para que no todos sean iguales
            valor = int(base + random.uniform(-2, 2))
            stats[attr] = max(1, min(20, valor)) # Mantener entre 1 y 20
        return stats

    def entrenar(self):
        """Simula el crecimiento de una temporada"""
        if self.ca < self.pa and self.edad < 30:
            crecimiento = random.randint(1, 5)
            self.ca = min(self.ca + crecimiento, self.pa)
            # Actualizamos atributos
            for attr in self.atributos:
                if random.random() > 0.5: # No todos los atributos suben a la vez
                    self.atributos[attr] = min(20, self.atributos[attr] + 1)
            print(f"¡{self.nombre} ha mejorado! Nuevo CA: {self.ca}")
        else:
            print(f"{self.nombre} ha alcanzado su techo o es muy mayor.")

