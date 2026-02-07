import sqlite3

def insertar_copas_completas():
    conn = sqlite3.connect("futbol_manager.db")
    cursor = conn.cursor()

    # Aseguramos que las columnas existan por si acaso
    try:
        cursor.execute("ALTER TABLE copas_clubes ADD COLUMN pais_id INTEGER")
        cursor.execute("ALTER TABLE copas_clubes ADD COLUMN tipo TEXT")
    except sqlite3.OperationalError:
        pass 

    copas = [
        # INTERNACIONALES (UEFA)
        ('UEFA Champions League', 'Europa', 'Grupos + Eliminatoria', 5000, 'Internacional', None),
        ('UEFA Europa League', 'Europa', 'Grupos + Eliminatoria', 3000, 'Internacional', None),
        ('UEFA Conference League', 'Europa', 'Grupos + Eliminatoria', 1500, 'Internacional', None), # <--- Añadida
        
        # NACIONALES (Copas Domésticas)
        ('Copa del Rey', 'Europa', 'Eliminatoria', 1500, 'Nacional', 11),        # España
        ('FA Cup', 'Europa', 'Eliminatoria', 1800, 'Nacional', 13),              # Inglaterra
        ('Coppa Italia', 'Europa', 'Eliminatoria', 1400, 'Nacional', 17),        # Italia
        ('DFB-Pokal', 'Europa', 'Eliminatoria', 1400, 'Nacional', 18),           # Alemania
        ('Coupe de France', 'Europa', 'Eliminatoria', 1300, 'Nacional', 12)       # Francia
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO copas_clubes 
        (nombre, continente, formato, recompensa_campeon, tipo, pais_id) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', copas)

    conn.commit()
    conn.close()
    print("Sistema de copas actualizado: Champions, Europa League y Conference League listas.")

if __name__ == "__main__":
    insertar_copas_completas()