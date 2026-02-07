import sqlite3

def poblar_todos_los_paises():
    conn = sqlite3.connect("futbol_manager.db")
    cursor = conn.cursor()

    # Formato: (Nombre, Continente, Ranking FIFA Inicial)
    paises_data = [
        # --- CONMEBOL (Sudamérica) ---
        ('Argentina', 'Sudamérica', 1), ('Brasil', 'Sudamérica', 5), ('Uruguay', 'Sudamérica', 11),
        ('Colombia', 'Sudamérica', 12), ('Ecuador', 'Sudamérica', 27), ('Perú', 'Sudamérica', 42),
        ('Chile', 'Sudamérica', 43), ('Venezuela', 'Sudamérica', 52), ('Paraguay', 'Sudamérica', 56),
        ('Bolivia', 'Sudamérica', 85),

        # --- UEFA (Europa) ---
        ('Francia', 'Europa', 2), ('España', 'Europa', 3), ('Inglaterra', 'Europa', 4),
        ('Bélgica', 'Europa', 6), ('Países Bajos', 'Europa', 7), ('Portugal', 'Europa', 8),
        ('Italia', 'Europa', 10), ('Croacia', 'Europa', 9), ('Alemania', 'Europa', 13),
        ('Suiza', 'Europa', 15), ('Dinamarca', 'Europa', 18), ('Ucrania', 'Europa', 22),
        ('Austria', 'Europa', 25), ('Polonia', 'Europa', 28), ('Hungría', 'Europa', 26),
        ('Suecia', 'Europa', 32), ('Gales', 'Europa', 29), ('Serbia', 'Europa', 33),
        ('Escocia', 'Europa', 39), ('Turquía', 'Europa', 40), ('República Checa', 'Europa', 36),
        ('Rumania', 'Europa', 46), ('Noruega', 'Europa', 44), ('Grecia', 'Europa', 49),
        ('Eslovaquia', 'Europa', 48), ('Eslovenia', 'Europa', 57), ('Irlanda', 'Europa', 60),
        ('Finlandia', 'Europa', 61), ('Albania', 'Europa', 62), ('Bosnia y Herzegovina', 'Europa', 74),
        ('Islandia', 'Europa', 72), ('Macedonia del Norte', 'Europa', 68), ('Montenegro', 'Europa', 70),
        ('Georgia', 'Europa', 75), ('Israel', 'Europa', 78), ('Bulgaria', 'Europa', 83),
        ('Luxemburgo', 'Europa', 87), ('Armenia', 'Europa', 95), ('Bielorrusia', 'Europa', 97),
        ('Kosovo', 'Europa', 102), ('Kazajistán', 'Europa', 100), ('Azerbaiyán', 'Europa', 112),
        ('Estonia', 'Europa', 123), ('Chipre', 'Europa', 125), ('Islas Feroe', 'Europa', 133),
        ('Letonia', 'Europa', 136), ('Lituania', 'Europa', 138), ('Moldavia', 'Europa', 153),
        ('Andorra', 'Europa', 164), ('Malta', 'Europa', 172), ('Gibraltar', 'Europa', 201),
        ('Liechtenstein', 'Europa', 202), ('San Marino', 'Europa', 210),

        # --- CONCACAF (Norte, Centroamérica y Caribe) ---
        ('Estados Unidos', 'Norteamérica', 14), ('México', 'Norteamérica', 16), ('Panamá', 'Norteamérica', 41),
        ('Canadá', 'Norteamérica', 45), ('Costa Rica', 'Norteamérica', 54), ('Jamaica', 'Norteamérica', 55),
        ('Honduras', 'Norteamérica', 78), ('El Salvador', 'Norteamérica', 81), ('Haití', 'Norteamérica', 90),
        ('Curazao', 'Norteamérica', 91), ('Trinidad y Tobago', 'Norteamérica', 96), ('Guatemala', 'Norteamérica', 108),
        ('Antigua y Barbuda', 'Norteamérica', 142), ('Surinam', 'Norteamérica', 144), ('San Cristóbal y Nieves', 'Norteamérica', 147),
        ('Nicaragua', 'Norteamérica', 134), ('República Dominicana', 'Norteamérica', 151), ('Puerto Rico', 'Norteamérica', 160),
        ('Santa Lucía', 'Norteamérica', 167), ('Cuba', 'Norteamérica', 169), ('Bermudas', 'Norteamérica', 171),
        ('Granada', 'Norteamérica', 174), ('San Vicente y las Granadinas', 'Norteamérica', 175), ('Belice', 'Norteamérica', 182),
        ('Montserrat', 'Norteamérica', 176), ('Barbados', 'Norteamérica', 178), ('Dominica', 'Norteamérica', 180),
        ('Guyana', 'Norteamérica', 154), ('Aruba', 'Norteamérica', 193), ('Islas Caimán', 'Norteamérica', 196),
        ('Bahamas', 'Norteamérica', 200), ('Islas Turcas y Caicos', 'Norteamérica', 206), ('Islas Vírgenes Británicas', 'Norteamérica', 207),
        ('Islas Vírgenes de los EE.UU.', 'Norteamérica', 208), ('Anguila', 'Norteamérica', 209),

        # --- CAF (África) ---
        ('Marruecos', 'África', 13), ('Senegal', 'África', 17), ('Nigeria', 'África', 30),
        ('Egipto', 'África', 36), ('Costa de Marfil', 'África', 38), ('Túnez', 'África', 41),
        ('Argelia', 'África', 43), ('Malí', 'África', 47), ('Camerún', 'África', 51),
        ('Sudáfrica', 'África', 59), ('Burkina Faso', 'África', 61), ('RD Congo', 'África', 63),
        ('Cabo Verde', 'África', 65), ('Ghana', 'África', 68), ('Guinea', 'África', 76),
        ('Guinea Ecuatorial', 'África', 79), ('Gabón', 'África', 84), ('Zambia', 'África', 86),
        ('Uganda', 'África', 92), ('Angola', 'África', 94), ('Benín', 'África', 98),
        ('Mauritania', 'África', 105), ('Namibia', 'África', 106), ('Madagascar', 'África', 109),
        ('Mozambique', 'África', 110), ('Kenia', 'África', 111), ('Congo', 'África', 113),
        ('Togo', 'África', 116), ('Libia', 'África', 118), ('Guinea-Bissau', 'África', 115),
        ('Tanzania', 'África', 119), ('Zimbabue', 'África', 122), ('Malaui', 'África', 125),
        ('Sierra Leona', 'África', 126), ('Sudán', 'África', 127), ('Níger', 'África', 129),
        ('República Centroafricana', 'África', 131), ('Gambia', 'África', 130), ('Ruanda', 'África', 133),
        ('Burundi', 'África', 140), ('Etiopía', 'África', 145), ('Botsuana', 'África', 146),
        ('Lesoto', 'África', 148), ('Liberia', 'África', 150), ('Eswatini', 'África', 156),
        ('Sudán del Sur', 'África', 167), ('Mauricio', 'África', 177), ('Chad', 'África', 181),
        ('Santo Tomé y Príncipe', 'África', 188), ('Yibuti', 'África', 192), ('Seychelles', 'África', 199),
        ('Eritrea', 'África', 202), ('Somalia', 'África', 198),

        # --- AFC (Asia) ---
        ('Japón', 'Asia', 17), ('Irán', 'Asia', 20), ('Corea del Sur', 'Asia', 23),
        ('Australia', 'Oceanía', 24), ('Qatar', 'Asia', 34), ('Arabia Saudita', 'Asia', 53),
        ('Irak', 'Asia', 58), ('Uzbekistán', 'Asia', 64), ('Emiratos Árabes Unidos', 'Asia', 67),
        ('Jordania', 'Asia', 71), ('Omán', 'Asia', 77), ('Baréin', 'Asia', 80),
        ('China', 'Asia', 88), ('Siria', 'Asia', 89), ('Palestina', 'Asia', 93),
        ('Tailandia', 'Asia', 101), ('Kirguistán', 'Asia', 104), ('Vietnam', 'Asia', 115),
        ('Corea del Norte', 'Asia', 118), ('Líbano', 'Asia', 120), ('India', 'Asia', 121),
        ('Tayikistán', 'Asia', 103), ('Malasia', 'Asia', 132), ('Kuwait', 'Asia', 137),
        ('Filipinas', 'Asia', 139), ('Turkmenistán', 'Asia', 143), ('Indonesia', 'Asia', 134),
        ('Yemén', 'Asia', 151), ('Afganistán', 'Asia', 158), ('Maldivas', 'Asia', 161),
        ('Singapur', 'Asia', 155), ('China Taipéi', 'Asia', 159), ('Myanmar', 'Asia', 163),
        ('Nepal', 'Asia', 178), ('Camboya', 'Asia', 179), ('Macao', 'Asia', 186),
        ('Bután', 'Asia', 184), ('Mongolia', 'Asia', 190), ('Laos', 'Asia', 189),
        ('Brunéi', 'Asia', 194), ('Bangladesh', 'Asia', 183), ('Timor-Leste', 'Asia', 196),
        ('Guam', 'Asia', 203), ('Pakistán', 'Asia', 197), ('Sri Lanka', 'Asia', 204),

        # --- OFC (Oceanía) ---
        ('Nueva Zelanda', 'Oceanía', 107), ('Islas Salomón', 'Oceanía', 132), ('Nueva Caledonia', 'Oceanía', 158),
        ('Tahití', 'Oceanía', 162), ('Fiyi', 'Oceanía', 168), ('Vanuatu', 'Oceanía', 170),
        ('Papúa Nueva Guinea', 'Oceanía', 165), ('Samoa Americana', 'Oceanía', 187), ('Islas Cook', 'Oceanía', 185),
        ('Samoa', 'Oceanía', 186), ('Tonga', 'Oceanía', 196)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO paises (nombre, continente, ranking_fifa) 
        VALUES (?, ?, ?)
    """, paises_data)

    conn.commit()
    conn.close()
    print(f"Base de datos poblada con {len(paises_data)} países del mundo.")

if __name__ == "__main__":
    poblar_todos_los_paises()