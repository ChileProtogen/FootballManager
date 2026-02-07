import sqlite3
import random

def gestionar_temporada(año_inicio, archivar_vieja=False):
    """
    Une la lógica de: 
    1. Archivar temporada anterior (si se indica).
    2. Generar el string de temporada actual (ej: '25/26').
    3. Generar el calendario completo para todas las ligas.
    """
    conn = sqlite3.connect("futbol_manager.db")
    cursor = conn.cursor()

    # --- 1. ARCHIVADO Y LIMPIEZA (Solo si termina una temporada) ---
    if archivar_vieja:
        temporada_vieja = f"{str(año_inicio-1)[-2:]}/{str(año_inicio)[-2:]}"
        
        # Mover al historial
        cursor.execute("""
            INSERT INTO historial_partidos 
            SELECT id, liga_id, copa_id, jornada, temporada, equipo_local_id, equipo_visitante_id, goles_local, goles_visitante 
            FROM partidos WHERE temporada = ? AND jugado = 1
        """, (temporada_vieja,))
        
        # Borrar de la tabla activa
        cursor.execute("DELETE FROM partidos WHERE temporada = ?", (temporada_vieja,))
        
        # Mantener solo 5 últimas temporadas en historial
        cursor.execute("SELECT DISTINCT temporada FROM historial_partidos ORDER BY temporada DESC")
        temps_historial = [r[0] for r in cursor.fetchall()]
        if len(temps_historial) > 5:
            for t in temps_historial[5:]:
                cursor.execute("DELETE FROM historial_partidos WHERE temporada = ?", (t,))
        
        print(f"✅ Temporada {temporada_vieja} archivada.")

    # --- 2. GENERACIÓN DE NUEVO CALENDARIO ---
    temp_actual = f"{str(año_inicio)[-2:]}/{str(año_inicio+1)[-2:]}"
    
    # Obtenemos todas las ligas
    cursor.execute("SELECT id, nombre FROM ligas")
    ligas = cursor.fetchall()

    for liga_id, liga_nom in ligas:
        cursor.execute("SELECT id FROM equipos WHERE liga_id = ?", (liga_id,))
        equipos = [row[0] for row in cursor.fetchall()]

        if not equipos: continue
        
        # Algoritmo de Círculo (Round Robin)
        if len(equipos) % 2 != 0: equipos.append(None)
        random.shuffle(equipos)
        
        n = len(equipos)
        partidos_temporada = []

        # Generar Ida (Jornadas 1 a n-1)
        for j in range(n - 1):
            for i in range(n // 2):
                local, visitante = equipos[i], equipos[n - 1 - i]
                if local and visitante:
                    # Alternamos localía cada jornada para equilibrio
                    if j % 2 == 0:
                        partidos_temporada.append((liga_id, j + 1, temp_actual, local, visitante))
                    else:
                        partidos_temporada.append((liga_id, j + 1, temp_actual, visitante, local))
            
            # Rotación del círculo
            equipos = [equipos[0]] + [equipos[-1]] + equipos[1:-1]

        # Generar Vuelta (Invertir localía de la ida)
        vueltas = []
        for p in partidos_temporada:
            # p[0]=liga_id, p[1]=jornada, p[2]=temp, p[3]=local, p[4]=visitante
            vueltas.append((p[0], p[1] + (n - 1), p[2], p[4], p[3]))

        # Inserción masiva
        cursor.executemany("""
            INSERT INTO partidos (liga_id, jornada, temporada, equipo_local_id, equipo_visitante_id)
            VALUES (?, ?, ?, ?, ?)
        """, partidos_temporada + vueltas)

    conn.commit()
    conn.close()
    print(f"🚀 Calendarios {temp_actual} generados para todas las ligas.")

# Ejemplo de uso para empezar la primera temporada:
if __name__ == "__main__":
    gestionar_temporada(2025) # Crea la 25/26