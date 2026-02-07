import sqlite3

def insertar_ligue_1():
    conn = sqlite3.connect("futbol_manager.db")
    cursor = conn.cursor()
    
    id_francia = 12

    # 1. Crear la liga vinculada a Francia (ID 12)
    cursor.execute('''
        INSERT OR IGNORE INTO ligas (pais_id, nombre, nivel) 
        VALUES (?, 'Ligue 1', 1)
    ''', (id_francia,))
    
    # 2. Obtener el ID asignado a la Ligue 1
    cursor.execute("SELECT id FROM ligas WHERE nombre = 'Ligue 1'")
    id_ligue_1 = cursor.fetchone()[0]

    # 3. Lista de equipos (liga_id, pais_id, nombre, presupuesto)
    # El PSG lidera con diferencia, seguido por el poderío de Mónaco y Lyon
    equipos = [
        (id_ligue_1, id_francia, "Paris Saint-Germain", 6000),
        (id_ligue_1, id_francia, "AS Monaco", 3800),
        (id_ligue_1, id_francia, "Olympique de Marseille", 3600),
        (id_ligue_1, id_francia, "Olympique Lyonnais", 3400),
        (id_ligue_1, id_francia, "Lille OSC", 3100),
        (id_ligue_1, id_francia, "OGC Nice", 2900),
        (id_ligue_1, id_francia, "Stade Rennais", 2700),
        (id_ligue_1, id_francia, "RC Lens", 2500),
        (id_ligue_1, id_francia, "Stade de Reims", 2100),
        (id_ligue_1, id_francia, "Toulouse FC", 1950),
        (id_ligue_1, id_francia, "Montpellier HSC", 1850),
        (id_ligue_1, id_francia, "RC Strasbourg", 2200),
        (id_ligue_1, id_francia, "FC Nantes", 1800),
        (id_ligue_1, id_francia, "Le Havre AC", 1600),
        (id_ligue_1, id_francia, "AJ Auxerre", 1650),
        (id_ligue_1, id_francia, "Angers SCO", 1550),
        (id_ligue_1, id_francia, "AS Saint-Étienne", 2000),
        (id_ligue_1, id_francia, "Stade Brestois 29", 2300) # Subida por Champions
    ]

    # 4. Inserción masiva
    try:
        cursor.executemany('''
            INSERT INTO equipos (liga_id, pais_id, nombre, presupuesto) 
            VALUES (?, ?, ?, ?)
        ''', equipos)
        conn.commit()
        print(f"Éxito: Ligue 1 (ID: {id_ligue_1}) poblada con 18 equipos franceses.")
    except sqlite3.IntegrityError:
        print("Aviso: Algunos equipos de la Ligue 1 ya existían.")
    finally:
        conn.close()

if __name__ == "__main__":
    insertar_ligue_1()