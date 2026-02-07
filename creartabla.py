import sqlite3

def asegurar_tablas_existentes():
    conn = sqlite3.connect("futbol_manager.db")
    cursor = conn.cursor()

    # Creamos la tabla de partidos si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS partidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        liga_id INTEGER,
        copa_id INTEGER,
        jornada INTEGER,
        temporada TEXT,
        equipo_local_id INTEGER,
        equipo_visitante_id INTEGER,
        goles_local INTEGER DEFAULT NULL,
        goles_visitante INTEGER DEFAULT NULL,
        jugado BOOLEAN DEFAULT 0,
        FOREIGN KEY(liga_id) REFERENCES ligas(id)
    )''')

    # Aprovechamos para crear la de historial por si acaso
    cursor.execute('''CREATE TABLE IF NOT EXISTS historial_partidos (
        id INTEGER PRIMARY KEY,
        liga_id INTEGER,
        copa_id INTEGER,
        jornada INTEGER,
        temporada TEXT,
        equipo_local_id INTEGER,
        equipo_visitante_id INTEGER,
        goles_local INTEGER,
        goles_visitante INTEGER
    )''')
    
    conn.commit()
    conn.close()
    print("✅ Tablas de sistema verificadas y listas.")

# Llama a esta función antes de FMGui
if __name__ == "__main__":
    asegurar_tablas_existentes()