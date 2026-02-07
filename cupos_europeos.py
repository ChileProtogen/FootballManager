import sqlite3
import random

def configurar_cupos_europeos():
    conn = sqlite3.connect("futbol_manager.db")
    cursor = conn.cursor()

    # Obtener IDs de las copas (Asegúrate de que coincidan con tu tabla copas_clubes)
    cursor.execute("SELECT id, nombre FROM copas_clubes")
    copas = {nombre: idx for idx, nombre in cursor.fetchall()}

    # Obtener IDs de las ligas
    cursor.execute("SELECT id, nombre FROM ligas")
    ligas = {nombre: idx for idx, nombre in cursor.fetchall()}

    reglas = []
    
    for liga_nom in ["Premier League", "La Liga", "Serie A", "Bundesliga"]:
        l_id = ligas[liga_nom]
        # Top 4 a Champions
        reglas.append((l_id, copas['UEFA Champions League'], 1, 4))
        # 5º a Europa League
        reglas.append((l_id, copas['UEFA Europa League'], 5, 5))
        # 6º a Conference
        reglas.append((l_id, copas['UEFA Conference League'], 6, 6))

    # Caso Francia (Ligue 1 - Top 3 directo, 4º previa, etc. Simplificamos a Top 3)
    l_id_fr = ligas["Ligue 1"]
    reglas.append((l_id_fr, copas['UEFA Champions League'], 1, 3))
    reglas.append((l_id_fr, copas['UEFA Europa League'], 4, 4))
    reglas.append((l_id_fr, copas['UEFA Conference League'], 5, 5))

    cursor.executemany("""
        INSERT INTO reglas_clasificacion (liga_id, copa_id, posicion_min, posicion_max)
        VALUES (?, ?, ?, ?)
    """, reglas)

    conn.commit()
    conn.close()
    print("Cupos europeos configurados para las 5 grandes ligas.")