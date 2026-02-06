import random
import os
from match_engine import simular_partido_mejorado
from liga import Liga
from potencial import Jugador as JugadorCompleto
from atributos import generar_nombre_aleatorio, generar_stats_jugador

class EquipoReal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.plantilla = []
        self.goles = 0
        self.nivel_medio = 0

    def generar_plantilla_inicial(self, cantidad=11):
        posiciones = ["Delantero", "Defensa", "Mediocentro"]
        for _ in range(cantidad):
            nombre = generar_nombre_aleatorio()
            pos = random.choice(posiciones)
            edad = random.randint(17, 25)
            # 1. Generamos los atributos desde atributos.py
            stats = generar_stats_jugador(pos)
            # 2. Creamos el objeto Jugador de potencial.py con esos atributos
            nuevo_jugador = JugadorCompleto(nombre, pos, edad, stats)
            self.plantilla.append(nuevo_jugador)
        self.actualizar_nivel_equipo()

    def actualizar_nivel_equipo(self):
        if self.plantilla:
            # Promedio de CA (0-200) convertido a escala 0-100
            suma_ca = sum(j.ca for j in self.plantilla)
            self.nivel_medio = (suma_ca / len(self.plantilla)) / 2

# --- FUNCIONES DE FLUJO DE JUEGO ---

def nueva_partida():
    nombres_clubes = ["Real Madrid", "FC Barcelona", "Atlético", "Sevilla", "Valencia", "Real Betis"]
    equipos = []
    
    print("\n🔨 Generando mundo y jugadores...")
    for nombre in nombres_clubes:
        e = EquipoReal(nombre)
        e.generar_plantilla_inicial()
        equipos.append(e)
    
    mi_liga = Liga("La Liga", equipos)
    mi_liga.generar_fixture()
    print("✅ Fixture generado. ¡Todos contra todos!")
    return mi_liga

def menu_principal():
    mi_liga = None
    
    while True:
        print("\n--- ⚽ FOOTBALL MANAGER CLONE ---")
        print("1. Nueva Partida")
        print("2. Cargar Partida")
        print("3. Salir")
        
        op = input("Seleccione una opción: ")
        
        if op == "1":
            mi_liga = nueva_partida()
            bucle_de_juego(mi_liga)
        elif op == "2":
            # Para cargar, creamos una instancia vacía de Liga y usamos su método
            mi_liga = Liga("Cargando...", [])
            if mi_liga.cargar_partida():
                # Nota: En una versión avanzada, aquí deberías reconstruir 
                # los objetos EquipoReal desde el JSON.
                bucle_de_juego(mi_liga)
        elif op == "3":
            print("¡Gracias por jugar!")
            break

def bucle_de_juego(liga):
    while liga.jornada_actual < len(liga.calendario):
        print(f"\n📅 JORNADA {liga.jornada_actual + 1} / {len(liga.calendario)}")
        print("1. Jugar todos los partidos de la jornada")
        print("2. Ver Tabla de Clasificación")
        print("3. Guardar y Salir al Menú")
        
        op = input(">> ")
        
        if op == "1":
            partidos = liga.calendario[liga.jornada_actual]
            for local_nom, vis_nom in partidos:
                # Buscamos los objetos equipo por su nombre
                local = next(e for e in liga.equipos if e.nombre == local_nom)
                visitante = next(e for e in liga.equipos if e.nombre == vis_nom)
                
                # Simulación
                simular_partido_mejorado(local, visitante)
                liga.registrar_resultado(local, visitante)
                
                # Evolución de jugadores tras el partido
                for equipo in [local, visitante]:
                    for j in equipo.plantilla:
                        j.entrenar()
                    equipo.actualizar_nivel_equipo()
            
            liga.jornada_actual += 1
            print(f"\n✅ Jornada {liga.jornada_actual} finalizada.")
            
        elif op == "2":
            liga.mostrar_tabla()
            
        elif op == "3":
            liga.guardar_partida()
            break

if __name__ == "__main__":
    menu_principal()