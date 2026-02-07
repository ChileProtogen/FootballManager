import random

def simular_partido_pro(local, visitante):
    """
    Simulador avanzado que usa CA, Atributos y Factor Campo.
    """
    # 1. Reset de partido
    local.goles, visitante.goles = 0, 0
    cronica = [f"🏟️ {local.nombre} vs {visitante.nombre}", "-"*40]

    # 2. Factor Campo: El local recibe un bono de +5% en su nivel efectivo
    nivel_local = local.nivel_medio * 1.05
    nivel_visitante = visitante.nivel_medio
    
    # Probabilidades base
    PROB_EVENTO = 0.18  # Un poco más de acción
    
    for minuto in range(1, 95): # Añadimos tiempo de descuento
        if random.random() < PROB_EVENTO:
            # Determinamos quién ataca basado en el peso de los niveles
            # Si el local tiene 150 y el visitante 100, el local ataca el 60% de las veces
            if random.random() < (nivel_local / (nivel_local + nivel_visitante)):
                atacante, defensor = local, visitante
            else:
                atacante, defensor = visitante, local

            # 3. Elección lógica del protagonista
            # Buscamos un delantero o medio para atacar
            delanteros = [j for j in atacante.plantilla if j.posicion == "Delantero"]
            if delanteros and random.random() < 0.7:
                protagonista = random.choice(delanteros)
            else:
                protagonista = random.choice(atacante.plantilla)

            # 4. Lógica de Resolución (Duelo de Atributos)
            # Obtenemos al portero rival
            portero_rival = next((j for j in defensor.plantilla if j.posicion == "Portero"), None)
            
            # El éxito depende de: (Remate del delantero + CA/10) vs (Reflejos Portero + CA/10)
            # Si no tienes los atributos a mano, usamos CA como base
            ataque_score = protagonista.stats.get("Remate", 10) + (protagonista.ca / 15)
            defensa_score = (portero_rival.stats.get("Reflejos", 10) if portero_rival else 10) + (defensor.nivel_medio / 15)

            # Añadimos azar al duelo
            if (ataque_score + random.uniform(0, 10)) > (defensa_score + random.uniform(0, 12)):
                atacante.goles += 1
                cronica.append(f"[{minuto}'] ⚽ ¡GOOOL de {protagonista.nombre}! Remate imparable. ({local.goles}-{visitante.goles})")
            else:
                # Evento de "Casi gol" o parada
                if random.random() < 0.3:
                    cronica.append(f"[{minuto}'] 🧤 ¡PARADÓN! El portero de {defensor.nombre} salva el remate de {protagonista.nombre}.")

            # 5. Disciplina (Tarjetas)
            if random.random() < 0.05:
                infractor = random.choice(defensor.plantilla)
                infractor.amarillas_acumuladas += 1
                if infractor.amarillas_acumuladas == 2:
                    cronica.append(f"[{minuto}'] 🟥 ¡EXPULSADO! {infractor.nombre} por doble amarilla.")
                else:
                    cronica.append(f"[{minuto}'] 🟨 Amarilla para {infractor.nombre} ({defensor.nombre}).")

    cronica.append("-"*40)
    cronica.append(f"🏁 FINAL: {local.nombre} {local.goles} - {visitante.nombre} {visitante.goles}")
    return cronica