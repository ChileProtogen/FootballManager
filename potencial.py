import random

class Jugador:
    def __init__(self, nombre, posicion, edad, atributos_dict):
        self.nombre = nombre
        self.posicion = posicion
        self.edad = edad
        self.atributos = atributos_dict
        
        # --- ESTADOS DE DISPONIBILIDAD ---
        self.lesionado = False
        self.dias_lesion = 0
        self.sancionado = False
        self.amarillas_acumuladas = 0
        
        # Potencial y Habilidad (Escala 0-200)
        self.pa = random.randint(100, 200) 
        promedio_atributos = sum(self.atributos.values()) / len(self.atributos)
        self.ca = int(promedio_atributos * 10)
        
        if self.ca > self.pa:
            self.pa = self.ca + 10

    @property
    def nivel_medio(self):
        """Si está disponible, aporta su CA; si no, su aporte es 0 o mínimo"""
        return (self.ca / 2) if not self.lesionado and not self.sancionado else 0

    def recuperar(self):
        """Avanza el tiempo de recuperación de lesiones y sanciones"""
        if self.lesionado:
            self.dias_lesion -= 1
            if self.dias_lesion <= 0:
                self.lesionado = False
                print(f"🏥 {self.nombre} ha recibido el alta médica.")
        
        if self.sancionado:
            self.sancionado = False
            print(f"⚖️ {self.nombre} ha cumplido su sanción.")

    def entrenar(self):
        """Simula el crecimiento o declive del jugador"""
        
        # CASO 1: El jugador está lesionado (Riesgo de empeorar)
        if self.lesionado:
            # 30% de probabilidad de que la lesión afecte su CA
            if random.random() < 0.30:
                perdida = random.randint(1, 3)
                self.ca = max(10, self.ca - perdida)
                
                # Bajamos un atributo al azar
                attr_random = random.choice(list(self.atributos.keys()))
                self.atributos[attr_random] = max(1, self.atributos[attr_random] - 1)
                
                print(f"⚠️ {self.nombre} ha perdido forma por la lesión. Nuevo CA: {self.ca}")
            return False

        # CASO 2: El jugador está sano y es joven (Progreso normal)
        if self.ca < self.pa and self.edad < 30:
            crecimiento = random.randint(1, 5)
            self.ca = min(self.ca + crecimiento, self.pa)
            
            for attr in self.atributos:
                if random.random() > 0.6: # Un poco más difícil subir stats individuales
                    if self.atributos[attr] < 20:
                        self.atributos[attr] += 1
            
            print(f"📈 {self.nombre} ha progresado. Nuevo CA: {self.ca}")
            return True
            
        # CASO 3: Declive por edad (Veteranos)
        elif self.edad >= 32:
            if random.random() < 0.4:
                caida = random.randint(1, 4)
                self.ca -= caida
                print(f"📉 {self.nombre} pierde nivel por la edad. Nuevo CA: {self.ca}")
            return False

        return False