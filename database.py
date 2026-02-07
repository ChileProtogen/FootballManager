import sqlite3

def inicializar_db_global():
    conn = sqlite3.connect("futbol_manager.db")
    cursor = conn.cursor()

    # 1. TABLA DE PAÍSES (El núcleo del sistema)
    cursor.execute('''CREATE TABLE IF NOT EXISTS paises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        continente TEXT,
        ranking_fifa INTEGER
    )''')

    # 2. TABLA DE LIGAS (Vinculada a un País)
    cursor.execute('''CREATE TABLE IF NOT EXISTS ligas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pais_id INTEGER,
        nombre TEXT NOT NULL UNIQUE,
        nivel INTEGER DEFAULT 1, -- 1 para primera división, 2 para segunda, etc.
        FOREIGN KEY(pais_id) REFERENCES paises(id)
    )''')

    # 3. TABLA DE EQUIPOS (Vinculada a una Liga y a un País)
    cursor.execute('''CREATE TABLE IF NOT EXISTS equipos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        liga_id INTEGER,
        pais_id INTEGER, 
        nombre TEXT NOT NULL UNIQUE,
        presupuesto INTEGER DEFAULT 2000,
        FOREIGN KEY(liga_id) REFERENCES ligas(id),
        FOREIGN KEY(pais_id) REFERENCES paises(id)
    )''')

    # 4. TABLA DE JUGADORES (Con Nacionalidad)
    cursor.execute('''CREATE TABLE IF NOT EXISTS jugadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipo_id INTEGER,
        nacionalidad_id INTEGER,
        nombre TEXT NOT NULL,
        posicion TEXT,
        ca INTEGER,
        pa INTEGER,
        edad INTEGER,
        FOREIGN KEY(equipo_id) REFERENCES equipos(id),
        FOREIGN KEY(nacionalidad_id) REFERENCES paises(id)
    )''')

    # 5. TABLA DE COPAS INTERNACIONALES (Clubes: Champions, Libertadores)
    cursor.execute('''CREATE TABLE IF NOT EXISTS copas_clubes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        continente TEXT, -- 'Europa', 'Sudamérica', 'Global'
        formato TEXT, -- 'Eliminatoria', 'Grupos + Eliminatoria'
        recompensa_campeon INTEGER
    )''')

    # 6. TABLA DE TORNEOS DE SELECCIONES (Mundial, Eurocopa, etc.)
    cursor.execute('''CREATE TABLE IF NOT EXISTS copas_selecciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        frecuencia_años INTEGER DEFAULT 4,
        proxima_edicion INTEGER, -- Año (ej. 2026)
        tipo TEXT -- 'Continental' o 'Mundial'
    )''')

    # 7. TABLA DE PARTICIPANTES EN COPAS (Para saber quién juega qué)
    cursor.execute('''CREATE TABLE IF NOT EXISTS participantes_copas (
        copa_id INTEGER,
        equipo_id INTEGER,
        temporada INTEGER,
        FOREIGN KEY(copa_id) REFERENCES copas_clubes(id),
        FOREIGN KEY(equipo_id) REFERENCES equipos(id)
    )''')

    # 8. TABLA DE ATRIBUTOS (Vinculada a un Jugador)
    cursor.execute('''CREATE TABLE IF NOT EXISTS atributos (
        jugador_id INTEGER PRIMARY KEY,
        remate INTEGER DEFAULT 10,
        pase INTEGER DEFAULT 10,
        regate INTEGER DEFAULT 10,
        entrada INTEGER DEFAULT 10,
        control INTEGER DEFAULT 10,
        vision INTEGER DEFAULT 10,
        posicionamiento INTEGER DEFAULT 10,
        anticipacion INTEGER DEFAULT 10,
        determinacion INTEGER DEFAULT 10,
        velocidad INTEGER DEFAULT 10,
        resistencia INTEGER DEFAULT 10,
        fuerza INTEGER DEFAULT 10,
        reflejos INTEGER DEFAULT 10,
        agilidad INTEGER DEFAULT 10,
        FOREIGN KEY(jugador_id) REFERENCES jugadores(id) ON DELETE CASCADE
    )''')

    conn.commit()
    conn.close()
    print("Base de datos Global terminada: Países, Nacionalidades y Copas integradas.")

if __name__ == "__main__":
    inicializar_db_global()