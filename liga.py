import json
import random

class Liga:
    def __init__(self, nombre, equipos):
        self.nombre = nombre
        self.equipos = equipos  # Lista de objetos Equipo
        # Inicializamos las estadísticas de cada equipo
        self.tabla = {e.nombre: {"PJ": 0, "G": 0, "E": 0, "P": 0, "GF": 0, "GC": 0, "Pts": 0} for e in equipos}
        self.calendario = []
        self.jornada_actual = 0

    def registrar_resultado(self, local, visitante):
        # Actualizar partidos jugados y goles
        self.tabla[local.nombre]["PJ"] += 1
        self.tabla[visitante.nombre]["PJ"] += 1
        self.tabla[local.nombre]["GF"] += local.goles
        self.tabla[local.nombre]["GC"] += visitante.goles
        self.tabla[visitante.nombre]["GF"] += visitante.goles
        self.tabla[visitante.nombre]["GC"] += local.goles

        # Asignar puntos
        if local.goles > visitante.goles:
            self.tabla[local.nombre]["G"] += 1
            self.tabla[local.nombre]["Pts"] += 3
            self.tabla[visitante.nombre]["P"] += 1
        elif local.goles < visitante.goles:
            self.tabla[visitante.nombre]["G"] += 1
            self.tabla[visitante.nombre]["Pts"] += 3
            self.tabla[local.nombre]["P"] += 1
        else:
            self.tabla[local.nombre]["E"] += 1
            self.tabla[visitante.nombre]["E"] += 1
            self.tabla[local.nombre]["Pts"] += 1
            self.tabla[visitante.nombre]["Pts"] += 1


    def mostrar_tabla(self):
        # Ordenar por Puntos, luego por Diferencia de Goles (GF - GC)
        tabla_ordenada = sorted(
            self.tabla.items(), 
            key=lambda x: (x[1]['Pts'], x[1]['GF'] - x[1]['GC']), 
            reverse=True
        )
        
        print(f"\n--- CLASIFICACIÓN: {self.nombre} ---")
        print(f"{'Pos':<4} {'Equipo':<15} {'PJ':<3} {'G':<3} {'E':<3} {'P':<3} {'GF':<3} {'GC':<3} {'Pts':<3}")
        for i, (nombre, stats) in enumerate(tabla_ordenada, 1):
            print(f"{i:<4} {nombre:<15} {stats['PJ']:<3} {stats['G']:<3} {stats['E']:<3} {stats['P']:<3} {stats['GF']:<3} {stats['GC']:<3} {stats['Pts']:<3}")

    def guardar_partida(self, archivo="partida.json"):
        datos = {
            "nombre_liga": self.nombre,
            "jornada_actual": self.jornada_actual,
            "tabla": self.tabla,
            "calendario": self.calendario
        }
        with open(archivo, 'w') as f:
            json.dump(datos, f, indent=4)
        print("\n💾 Partida guardada exitosamente.")

    def cargar_partida(self, archivo="partida.json"):
        try:
            with open(archivo, 'r') as f:
                datos = json.load(f)
            self.nombre = datos["nombre_liga"]
            self.jornada_actual = datos["jornada_actual"]
            self.tabla = datos["tabla"]
            self.calendario = datos["calendario"]
            print("\n📂 Partida cargada exitosamente.")
            return True
        except FileNotFoundError:
            print("\n❌ No se encontró ningún archivo de guardado.")
            return False