import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random

# --- IMPORTACIONES DE TUS MÓDULOS ---
# Asegúrate de que estos nombres coincidan con tus archivos
from match_engine import simular_partido_pro 
from calendario import generar_calendario_espejo

class EquipoReal:
    def __init__(self, id_db, nombre, presupuesto=2000, id_liga=None):
        self.id_db = id_db
        self.nombre = nombre
        self.presupuesto = presupuesto
        self.id_liga = id_liga  # <--- Añadimos esto
        self.plantilla = []
        self.entrenador = None
        self.nivel_medio = 0
        
    def cargar_plantilla_desde_db(self):
        """Carga jugadores y sus atributos técnicos de la DB"""
        conn = sqlite3.connect("futbol_manager.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT j.nombre, j.posicion, j.ca, j.pa, j.edad, 
                   a.remate, a.pase, a.vision, a.reflejos, a.velocidad
            FROM jugadores j
            JOIN atributos a ON j.id = a.jugador_id
            WHERE j.equipo_id = ?
        """, (self.id_db,))
        
        filas = cursor.fetchall()
        self.plantilla = []
        for f in filas:
            # Creamos un objeto simple de jugador con acceso a sus stats
            jugador = type('Jugador', (), {
                'nombre': f[0], 'posicion': f[1], 'ca': f[2], 'pa': f[3], 'edad': f[4],
                'stats': {"Remate": f[5], "Pase": f[6], "Visión": f[7], "Reflejos": f[8], "Velocidad": f[9]},
                'amarillas_acumuladas': 0, 'lesionado': False, 'sancionado': False
            })
            self.plantilla.append(jugador)
        conn.close()
        self.actualizar_nivel_equipo()

    def actualizar_nivel_equipo(self):
        """Calcula el nivel basado en el CA y el bonus del DT"""
        disponibles = [j.ca for j in self.plantilla if not j.lesionado and not j.sancionado]
        if disponibles:
            ca_promedio = sum(disponibles) / len(disponibles)
            # El DT aporta un multiplicador (ej: Nivel 1.2 es un 20% extra)
            multiplicador = self.entrenador.nivel if self.entrenador else 0.8
            self.nivel_medio = ca_promedio * multiplicador
        else:
            self.nivel_medio = 10

class FMGui:
    def __init__(self, root, mi_equipo_nombre):
        self.root = root
        self.mi_equipo_nombre = mi_equipo_nombre
        self.anio_actual = 2025
        self.temporada_str = "25/26"
        self.jornada_actual = 0
        
        self.preparar_juego()
        self.setup_ui()

    def preparar_juego(self):
        conn = sqlite3.connect("futbol_manager.db")
        cursor = conn.cursor()

        # 1. Cargar Equipos (incluyendo liga_id)
        cursor.execute("SELECT id, nombre, presupuesto, liga_id FROM equipos") # Añadimos liga_id
        filas_equipos = cursor.fetchall()
        
        self.equipos = []
        for id_db, nombre, presupuesto, l_id in filas_equipos:
            eq = EquipoReal(id_db, nombre, presupuesto, id_liga=l_id) # Pasamos l_id
            eq.cargar_plantilla_desde_db()
            self.equipos.append(eq)

        # 2. Generar/Verificar Calendario
        generar_calendario_espejo(self.anio_actual)
        
        # 3. IDENTIFICAR AL USUARIO PRIMERO
        try:
            self.user_team = next(e for e in self.equipos if e.nombre == self.mi_equipo_nombre)
        except StopIteration:
            print(f"⚠️ No se encontró '{self.mi_equipo_nombre}', usando primero de la lista.")
            self.user_team = self.equipos[0]

        # 4. AHORA SÍ: Guardar el ID de la liga del usuario
        self.mi_liga_id = self.user_team.id_liga 

        # 5. Sincronizar jornada
        cursor.execute("""
            SELECT MAX(jornada) FROM partidos 
            WHERE jugado = 1 AND temporada = ? AND liga_id = ?
        """, (self.temporada_str, self.mi_liga_id))
        
        res = cursor.fetchone()[0]
        self.jornada_actual = res if res else 0
        conn.close()
        
    def setup_ui(self):
        self.root.state('zoomed')
        self.root.configure(bg="#121212")
        
        # --- Sidebar ---
        sidebar = tk.Frame(self.root, width=250, bg="#1a252f")
        sidebar.pack(side="left", fill="y")
        
        tk.Label(sidebar, text="DOF MANAGER", fg="#3498db", bg="#1a252f", font=("Impact", 28)).pack(pady=30)
        
        btn_params = {"bg": "#34495e", "fg": "white", "font": ("Segoe UI", 11, "bold"), "height": 2, "cursor": "hand2", "relief": "flat"}
        tk.Button(sidebar, text="Siguiente Jornada", command=self.jugar_jornada, **btn_params).pack(fill="x", padx=20, pady=10)
        tk.Button(sidebar, text="Ver Clasificación", command=self.actualizar_tabla, **btn_params).pack(fill="x", padx=20, pady=10)
        tk.Button(sidebar, text="Mi Plantilla", command=self.ver_plantilla_usuario, **btn_params).pack(fill="x", padx=20, pady=10)

        # --- Main Area ---
        self.main = tk.Frame(self.root, bg="#121212")
        self.main.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Header con Presupuesto y Jornada
        header = tk.Frame(self.main, bg="#121212")
        header.pack(fill="x")
        
        self.lbl_jornada = tk.Label(header, text=f"TEMPORADA {self.temporada_str} - JORNADA {self.jornada_actual + 1}", 
                                    fg="white", bg="#121212", font=("Segoe UI", 18, "bold"))
        self.lbl_jornada.pack(side="left")
        
        self.lbl_presupuesto = tk.Label(header, text=f"Presupuesto: {self.user_team.presupuesto}M 💰", 
                                        fg="#f1c40f", bg="#121212", font=("Segoe UI", 14, "bold"))
        self.lbl_presupuesto.pack(side="right")

        # Tabla de Clasificación
        cols = ("Pos", "Equipo", "PJ", "G", "E", "P", "Pts", "DG")
        self.tree = ttk.Treeview(self.main, columns=cols, show="headings", height=15)
        for c in cols: 
            self.tree.heading(c, text=c)
            self.tree.column(c, width=80, anchor="center")
        self.tree.column("Equipo", width=250, anchor="w")
        self.tree.pack(fill="x", pady=20)

        # Consola de Resultados
        self.txt_console = tk.Text(self.main, height=12, bg="#000", fg="#2ecc71", font=("Consolas", 10), padx=10, pady=10)
        self.txt_console.pack(fill="both", expand=True)
        
        self.actualizar_tabla()

    def jugar_jornada(self):
        conn = sqlite3.connect("futbol_manager.db")
        cursor = conn.cursor()
        # En FMGui.jugar_jornada
        cursor.execute("""
            SELECT equipo_local_id, equipo_visitante_id FROM partidos 
            WHERE jornada = ? AND temporada = ? AND jugado = 0 AND liga_id = ?
        """, (self.jornada_actual + 1, self.temporada_str, self.mi_liga_id))
        
        # Traer partidos de la jornada desde la DB
        cursor.execute("""
            SELECT equipo_local_id, equipo_visitante_id FROM partidos 
            WHERE jornada = ? AND temporada = ? AND jugado = 0
        """, (self.jornada_actual + 1, self.temporada_str))
        partidos = cursor.fetchall()

        if not partidos:
            messagebox.showinfo("Fin", "No hay más partidos en esta temporada.")
            return

        self.txt_console.delete("1.0", tk.END)
        self.txt_console.insert(tk.END, f">>> SIMULANDO JORNADA {self.jornada_actual + 1}...\n\n")

        for id_loc, id_vis in partidos:
            loc = next(e for e in self.equipos if e.id_db == id_loc)
            vis = next(e for e in self.equipos if e.id_db == id_vis)
            
            # Simulamos con el motor PRO
            cronica = simular_partido_pro(loc, vis)
            
            # Guardamos resultado en DB
            cursor.execute("""
                UPDATE partidos SET goles_local = ?, goles_visitante = ?, jugado = 1 
                WHERE equipo_local_id = ? AND equipo_visitante_id = ? AND temporada = ?
            """, (loc.goles, vis.goles, id_loc, id_vis, self.temporada_str))
            
            self.txt_console.insert(tk.END, f"• {loc.nombre} {loc.goles} - {vis.goles} {vis.nombre}\n")
            self.root.update() # Para que se vea en tiempo real

        conn.commit()
        conn.close()
        
        self.jornada_actual += 1
        self.lbl_jornada.config(text=f"TEMPORADA {self.temporada_str} - JORNADA {self.jornada_actual + 1}")
        self.actualizar_tabla()

    def actualizar_tabla(self):
        """Calcula la tabla directamente de los resultados en la DB"""
        for item in self.tree.get_children(): self.tree.delete(item)
        
        conn = sqlite3.connect("futbol_manager.db")
        cursor = conn.cursor()

        # Consulta SQL maestra para clasificación
        cursor.execute("""
            SELECT e.nombre,
                COUNT(p.id) as PJ,
                SUM(CASE WHEN (e.id = p.equipo_local_id AND p.goles_local > p.goles_visitante) OR 
                             (e.id = p.equipo_visitante_id AND p.goles_visitante > p.goles_local) THEN 1 ELSE 0 END) as G,
                SUM(CASE WHEN p.goles_local = p.goles_visitante THEN 1 ELSE 0 END) as E,
                SUM(CASE WHEN (e.id = p.equipo_local_id AND p.goles_local < p.goles_visitante) OR 
                             (e.id = p.equipo_visitante_id AND p.goles_visitante < p.goles_local) THEN 1 ELSE 0 END) as P,
                SUM(CASE WHEN e.id = p.equipo_local_id THEN p.goles_local ELSE p.goles_visitante END) -
                SUM(CASE WHEN e.id = p.equipo_local_id THEN p.goles_visitante ELSE p.goles_local END) as DG,
                SUM(CASE WHEN (e.id = p.equipo_local_id AND p.goles_local > p.goles_visitante) OR 
                             (e.id = p.equipo_visitante_id AND p.goles_visitante > p.goles_local) THEN 3
                         WHEN p.goles_local = p.goles_visitante THEN 1 ELSE 0 END) as Pts
            FROM equipos e
            JOIN partidos p ON (e.id = p.equipo_local_id OR e.id = p.equipo_visitante_id)
            WHERE p.jugado = 1 AND p.temporada = ?
            GROUP BY e.id
            ORDER BY Pts DESC, DG DESC
        """, (self.temporada_str,))

        for i, row in enumerate(cursor.fetchall(), 1):
            self.tree.insert("", "end", values=(i, row[0], row[1], row[2], row[3], row[4], row[6], row[5]))
        
        conn.close()

    def ver_plantilla_usuario(self):
        """Muestra los atributos detallados de tus jugadores"""
        v = tk.Toplevel(self.root)
        v.title(f"Plantilla: {self.user_team.nombre}")
        v.geometry("700x400")
        v.configure(bg="#1a252f")
        
        cols = ("Nombre", "Pos", "Edad", "CA", "Remate", "Pase", "Reflejos")
        t = ttk.Treeview(v, columns=cols, show="headings")
        for c in cols: 
            t.heading(c, text=c)
            t.column(c, width=90, anchor="center")
        
        for j in self.user_team.plantilla:
            t.insert("", "end", values=(j.nombre, j.posicion, j.edad, j.ca, 
                                        j.stats["Remate"], j.stats["Pase"], j.stats["Reflejos"]))
        t.pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == "__main__":
    # Aquí deberías llamar a tu selector de equipo primero
    # Por ahora forzamos uno para probar
    root = tk.Tk()
    app = FMGui(root, "FC Barcelona") # Cambia por el nombre que elijas
    root.mainloop()