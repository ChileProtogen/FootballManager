import sqlite3
import random

def generar_calendario_espejo(año_inicio):
    conn = sqlite3.connect("futbol_manager.db")
    cursor = conn.cursor()

    temporada_act = f"{str(año_inicio)[-2:]}/{str(año_inicio+1)[-2:]}"
    
    # --- EVITAR DUPLICADOS ---
    cursor.execute("SELECT COUNT(*) FROM partidos WHERE temporada = ?", (temporada_act,))
    if cursor.fetchone()[0] > 0:
        print(f"⚠️ El calendario {temporada_act} ya existe en la DB.")
        conn.close()
        return

    cursor.execute("SELECT id FROM ligas")
    ligas = [r[0] for r in cursor.fetchall()]

    for liga_id in ligas:
        cursor.execute("SELECT id FROM equipos WHERE liga_id = ?", (liga_id,))
        equipos = [r[0] for r in cursor.fetchall()]
        
        # Manejo de impares para el Round Robin
        if len(equipos) % 2 != 0:
            equipos.append(None) # El None representa que un equipo descansa
        
        random.shuffle(equipos)
        n = len(equipos)
        num_jornadas_vuelta = n - 1
        
        primera_vuelta = []
        copia_equipos = list(equipos)

        for i in range(num_jornadas_vuelta):
            jornada = i + 1
            for j in range(n // 2):
                local = copia_equipos[j]
                visitante = copia_equipos[n - 1 - j]
                
                # LA CONDICIÓN CRÍTICA: Solo guardar si ambos existen (no son None)
                # Y por seguridad lógica, que no sean el mismo ID (aunque el algoritmo lo evita)
                if local is not None and visitante is not None and local != visitante:
                    if i % 2 == 0:
                        primera_vuelta.append((liga_id, jornada, temporada_act, local, visitante))
                    else:
                        primera_vuelta.append((liga_id, jornada, temporada_act, visitante, local))
            
            # Rotación: el primero fijo, los demás rotan
            copia_equipos.insert(1, copia_equipos.pop())

        # --- GENERAR SEGUNDA VUELTA (Espejo) ---
        segunda_vuelta = []
        for p in primera_vuelta:
            liga, jorn, temp, loc, vis = p
            segunda_vuelta.append((liga, jorn + num_jornadas_vuelta, temp, vis, loc))

        cursor.executemany("""
            INSERT INTO partidos (liga_id, jornada, temporada, equipo_local_id, equipo_visitante_id)
            VALUES (?, ?, ?, ?, ?)
        """, primera_vuelta + segunda_vuelta)

    conn.commit()
    conn.close()
    print(f"✅ Calendarios {temporada_act} generados sin errores de equipo nulo.")