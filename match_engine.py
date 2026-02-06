import random
import time

class Jugador:
    def __init__(self, nombre, nivel):
        # Simplificamos a un nivel general para el cálculo de dominio
        self.nombre = nombre
        self.nivel = nivel # 1 al 100

class Equipo:
    def __init__(self, nombre, nivel_medio):
        self.nombre = nombre
        self.nivel_medio = nivel_medio
        self.goles = 0

def simular_partido_mejorado(local, visitante):
    # 1. Calculamos la ventaja de calidad
    # Si local tiene 80 y visitante 70, la diferencia es 10.
    diferencia = local.nivel_medio - visitante.nivel_medio
    
    # Probabilidad base de que ocurra algo en un minuto dado (ej. 10%)
    PROB_EVENTO = 0.12 
    
    # Sesgo: Qué porcentaje de esos eventos son para el local
    # Si son iguales, es 0.5 (50%). Si el local es mejor, sube de 0.5
    sesgo_local = 0.5 + (diferencia / 100) 
    # Limitamos el sesgo para que no sea 100% o 0%
    sesgo_local = max(0.2, min(0.8, sesgo_local))

    print(f"🏟️  {local.nombre} ({local.nivel_medio}) vs {visitante.nombre} ({visitante.nivel_medio})")
    print(f"📈 Probabilidad de ataque local: {sesgo_local*100:.1f}%")
    print("-" * 40)

    for minuto in range(1, 91):
        # ¿Ocurre una jugada en este minuto?
        if random.random() < PROB_EVENTO:
            
            # ¿Quién ataca? Basado en el sesgo de calidad
            if random.random() < sesgo_local:
                atacante, defensor = local, visitante
            else:
                atacante, defensor = visitante, local

            # Lógica de resolución de la jugada (Simplificada)
            # La calidad del atacante vs la del defensor influye en el gol
            print(f"[{minuto}'] Ocasión clara para el {atacante.nombre}...")
            
            suerte = random.randint(-20, 20)
            if (atacante.nivel_medio + suerte) > (defensor.nivel_medio + 15):
                atacante.goles += 1
                print(f"⚽ ¡GOOOOOL! {atacante.nombre} {local.goles}-{visitante.goles} {visitante.nombre}")
            else:
                print(f"🧤 La jugada termina en nada.")
            
            time.sleep(1) # Para seguir la narración

    print("-" * 40)
    print(f"FINAL: {local.nombre} {local.goles} - {visitante.nombre} {visitante.goles}")

# --- PRUEBA ---
madrid = Equipo("Real Madrid", 88)
getafe = Equipo("Getafe", 74)

simular_partido_mejorado(madrid, getafe)