import random
import time

def simular_partido_mejorado(local, visitante):
    """
    Simula un partido integrando goles, tarjetas y lesiones.
    Las bajas afectan el rendimiento del equipo en tiempo real.
    """
    # 1. Ajuste inicial de goles
    local.goles = 0
    visitante.goles = 0
    
    # Probabilidades de eventos (por cada minuto con jugada)
    PROB_EVENTO = 0.15 
    PROB_LESION = 0.03   # 3% de que una jugada termine en lesión
    PROB_TARJETA = 0.08  # 8% de que haya amonestación
    PROB_ROJA_DIR = 0.01 # 1% roja directa

    print(f"\n🏟️  INICIA EL ENCUENTRO: {local.nombre} vs {visitante.nombre}")
    print("-" * 50)

    for minuto in range(1, 91):
        # Recalculamos el sesgo cada minuto por si hubo expulsados/lesionados
        diferencia = local.nivel_medio - visitante.nivel_medio
        sesgo_local = max(0.2, min(0.8, 0.5 + (diferencia / 100)))

        if random.random() < PROB_EVENTO:
            # Determinamos quién tiene la posesión
            if random.random() < sesgo_local:
                atacante, defensor = local, visitante
            else:
                atacante, defensor = visitante, local

            # Elegimos un jugador al azar de la plantilla que esté en el campo (no lesionado/sancionado)
            # Nota: Asumimos que los primeros 11 son los que están jugando
            protagonista = random.choice([j for j in atacante.plantilla if not j.lesionado and not j.sancionado])
            
            # --- POSIBLE LESIÓN ---
            if random.random() < PROB_LESION:
                protagonista.lesionado = True
                protagonista.dias_lesion = random.randint(1, 6)
                print(f"[{minuto}'] 🚑 ¡MALAS NOTICIAS! {protagonista.nombre} ({atacante.nombre}) se retira lesionado.")
                atacante.actualizar_nivel_equipo() # El nivel baja al instante
                continue # Se pierde la jugada por la lesión

            # --- LÓGICA DE GOLES ---
            suerte = random.randint(-20, 20)
            if (atacante.nivel_medio + suerte) > (defensor.nivel_medio + 15):
                atacante.goles += 1
                print(f"[{minuto}'] ⚽ ¡GOOOOOL de {protagonista.nombre}! {local.nombre} {local.goles}-{visitante.goles} {visitante.nombre}")
            
            # --- LÓGICA DE TARJETAS ---
            else:
                random_disciplina = random.random()
                if random_disciplina < PROB_ROJA_DIR:
                    protagonista.sancionado = True
                    print(f"[{minuto}'] 🟥 ¡ROJA DIRECTA! {protagonista.nombre} ({atacante.nombre}) a la calle.")
                    atacante.actualizar_nivel_equipo()
                
                elif random_disciplina < PROB_TARJETA:
                    protagonista.amarillas_acumuladas += 1
                    if protagonista.amarillas_acumuladas >= 2:
                        protagonista.sancionado = True
                        protagonista.amarillas_acumuladas = 0
                        print(f"[{minuto}'] 🟨🟨 Segunda amarilla para {protagonista.nombre}. 🟥 ¡EXPULSADO!")
                        atacante.actualizar_nivel_equipo()
                    else:
                        print(f"[{minuto}'] 🟨 Tarjeta amarilla para {protagonista.nombre} ({atacante.nombre}).")

            # Pequeña pausa para fluidez visual
            time.sleep(0.3) 

    print("-" * 50)
    print(f"🏁 FINAL: {local.nombre} {local.goles} - {visitante.nombre} {visitante.goles}\n")