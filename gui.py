import tkinter as tk
from tkinter import ttk, messagebox
import random
from liga import Liga
from match_engine import simular_partido_mejorado
from potencial import Jugador as JugadorCompleto
from atributos import generar_nombre_aleatorio, generar_stats_jugador, crear_jugadores_libres

# --- Lógica de Equipo ---
class EquipoReal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.plantilla = []
        self.presupuesto = 1000  # Monedas iniciales
        self.goles = 0
        self.nivel_medio = 0

    def generar_plantilla_inicial(self, cantidad=15):
        posiciones = ["Delantero", "Defensa", "Mediocentro"]
        for _ in range(cantidad):
            nombre = generar_nombre_aleatorio()
            pos = random.choice(posiciones)
            edad = random.randint(17, 34)
            stats = generar_stats_jugador(pos)
            nuevo_jugador = JugadorCompleto(nombre, pos, edad, stats)
            self.plantilla.append(nuevo_jugador)
        self.actualizar_nivel_equipo()

    def actualizar_nivel_equipo(self):
        disponibles = [j.ca for j in self.plantilla if not j.lesionado and not j.sancionado]
        if disponibles:
            self.nivel_medio = (sum(disponibles) / len(disponibles)) / 2
        else:
            self.nivel_medio = 10

# --- Interfaz Principal ---
class FMGui:
    def __init__(self, root):
        self.root = root
        self.root.title("PYTHON FOOTBALL MANAGER - PRO")
        self.root.geometry("1100x750")
        self.root.configure(bg="#121212")

        self.preparar_juego()
        self.setup_styles()
        self.setup_ui()

    def preparar_juego(self):
        nombres = ["Real Madrid", "Barcelona", "Atlético", "Sevilla", "Betis", "Valencia"]
        equipos = [EquipoReal(n) for n in nombres]
        for e in equipos: e.generar_plantilla_inicial()
        
        self.liga = Liga("La Liga", equipos)
        self.liga.generar_fixture()
        self.liga.mercado_libres = crear_jugadores_libres(10)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e1e1e", foreground="white", 
                        fieldbackground="#1e1e1e", borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#2c3e50", foreground="white", 
                        font=("Segoe UI", 10, "bold"), padding=5)
        style.map("Treeview", background=[('selected', '#3498db')])

    def setup_ui(self):
        sidebar = tk.Frame(self.root, width=220, bg="#1a252f")
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="FM CLONE", fg="#3498db", bg="#1a252f", font=("Impact", 26)).pack(pady=25)
        
        self.crear_boton(sidebar, "Siguiente Jornada", self.jugar_jornada)
        self.crear_boton(sidebar, "Mercado Fichajes", self.abrir_mercado)
        self.crear_boton(sidebar, "Ver Clasificación", self.actualizar_tabla)
        self.crear_boton(sidebar, "Guardar Partida", self.liga.guardar_partida)

        main = tk.Frame(self.root, bg="#121212")
        main.pack(side="right", expand=True, fill="both", padx=25, pady=20)

        header_frame = tk.Frame(main, bg="#121212")
        header_frame.pack(fill="x")

        self.lbl_jornada = tk.Label(header_frame, text=f"Jornada {self.liga.jornada_actual + 1}", 
                                    fg="white", bg="#121212", font=("Segoe UI", 20, "bold"))
        self.lbl_jornada.pack(side="left")

        self.lbl_presupuesto = tk.Label(header_frame, text=f"Presupuesto: {self.liga.equipos[0].presupuesto} 💰", 
                                        fg="#f1c40f", bg="#121212", font=("Segoe UI", 14, "bold"))
        self.lbl_presupuesto.pack(side="right")

        cols = ("Pos", "Equipo", "PJ", "Pts", "DG")
        self.tree = ttk.Treeview(main, columns=cols, show="headings", height=8)
        config_cols = {"Pos": 50, "Equipo": 250, "PJ": 60, "Pts": 60, "DG": 60}
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=config_cols[c], anchor="center")
        self.tree.column("Equipo", anchor="w")
        
        self.tree.pack(fill="x", pady=10)
        self.tree.bind("<Double-1>", self.on_double_click)

        tk.Label(main, text="PANEL DE NOTICIAS Y RESULTADOS", fg="#bdc3c7", bg="#121212", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.txt_resultados = tk.Text(main, height=12, bg="#0d0d0d", fg="#2ecc71", 
                                      font=("Consolas", 10), relief="flat", padx=10, pady=10)
        self.txt_resultados.pack(fill="x", pady=5)

        self.actualizar_tabla()

    def crear_boton(self, parent, texto, comando):
        tk.Button(parent, text=texto, command=comando, bg="#34495e", fg="white", 
                  activebackground="#2980b9", relief="flat", font=("Segoe UI", 10), 
                  height=2, cursor="hand2").pack(fill="x", padx=20, pady=8)

    def actualizar_tabla(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        tabla_ord = sorted(self.liga.tabla.items(), key=lambda x: (x[1]['Pts'], x[1]['GF']-x[1]['GC']), reverse=True)
        for i, (nombre, s) in enumerate(tabla_ord, 1):
            dg = s["GF"] - s["GC"]
            self.tree.insert("", "end", iid=nombre, values=(i, nombre, s["PJ"], s["Pts"], dg))
        self.lbl_presupuesto.config(text=f"Presupuesto: {self.liga.equipos[0].presupuesto} 💰")

    def jugar_jornada(self):
        if self.liga.jornada_actual < len(self.liga.calendario):
            self.txt_resultados.delete("1.0", tk.END)
            partidos = self.liga.calendario[self.liga.jornada_actual]
            
            for loc_n, vis_n in partidos:
                loc = next(e for e in self.liga.equipos if e.nombre == loc_n)
                vis = next(e for e in self.liga.equipos if e.nombre == vis_n)
                
                simular_partido_mejorado(loc, vis)
                self.liga.registrar_resultado(loc, vis)
                
                if loc.goles > vis.goles: loc.presupuesto += 100
                elif vis.goles > loc.goles: vis.presupuesto += 100
                else:
                    loc.presupuesto += 40
                    vis.presupuesto += 40

                self.txt_resultados.insert(tk.END, f" ✔ {loc.nombre.ljust(15)} {loc.goles} - {vis.goles} {vis_n}\n")
                
                for equipo in [loc, vis]:
                    for p in equipo.plantilla:
                        p.recuperar()
                        p.entrenar()
                    equipo.actualizar_nivel_equipo()

            self.liga.mercado_libres = crear_jugadores_libres(10)
            self.liga.jornada_actual += 1
            self.lbl_jornada.config(text=f"Jornada {self.liga.jornada_actual + 1}")
            self.actualizar_tabla()
        else:
            messagebox.showinfo("Liga Finalizada", "Has completado el calendario.")

    def abrir_mercado(self):
        v_mercado = tk.Toplevel(self.root)
        v_mercado.title("MERCADO DE FICHAJES")
        v_mercado.geometry("750x550")
        v_mercado.configure(bg="#1a252f")

        user_team = self.liga.equipos[0]
        
        tk.Label(v_mercado, text=f"Presupuesto Disponible: {user_team.presupuesto} 💰", 
                 fg="#f1c40f", bg="#1a252f", font=("Segoe UI", 12, "bold")).pack(pady=15)

        # AHORA CON PA
        cols = ("ID", "Nombre", "Pos", "CA", "PA", "Precio")
        t_m = ttk.Treeview(v_mercado, columns=cols, show="headings")
        config_m = {"ID": 40, "Nombre": 180, "Pos": 80, "CA": 60, "PA": 60, "Precio": 100}
        
        for c in cols:
            t_m.heading(c, text=c)
            t_m.column(c, width=config_m[c], anchor="center")
        
        for i, j in enumerate(self.liga.mercado_libres):
            precio = j.ca * 5
            t_m.insert("", "end", iid=i, values=(i, j.nombre, j.posicion, j.ca, j.pa, precio))
        
        t_m.pack(expand=True, fill="both", padx=20)

        def confirmar_fichaje():
            sel = t_m.focus()
            if not sel: return
            idx = int(sel)
            jugador = self.liga.mercado_libres[idx]
            coste = jugador.ca * 5
            
            if user_team.presupuesto >= coste:
                if messagebox.askyesno("Confirmar", f"¿Fichar a {jugador.nombre} por {coste}💰?"):
                    user_team.presupuesto -= coste
                    user_team.plantilla.append(self.liga.mercado_libres.pop(idx))
                    user_team.actualizar_nivel_equipo()
                    self.actualizar_tabla()
                    v_mercado.destroy()
            else:
                messagebox.showwarning("Fondos insuficientes", "No tienes suficiente dinero.")

        tk.Button(v_mercado, text="FICHAR JUGADOR", command=confirmar_fichaje, 
                  bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), height=2).pack(pady=15)

    def on_double_click(self, event=None):
        item_id = self.tree.focus()
        if not item_id: return
        equipo = next(e for e in self.liga.equipos if e.nombre == item_id)
        
        v = tk.Toplevel(self.root)
        v.title(f"Plantilla - {equipo.nombre}")
        v.geometry("850x500")
        v.configure(bg="#1a252f")

        # AHORA CON PA TAMBIÉN EN PLANTILLA
        cols = ("Nombre", "Pos", "Edad", "CA", "PA", "Estado")
        t = ttk.Treeview(v, columns=cols, show="headings")
        config_p = {"Nombre": 180, "Pos": 80, "Edad": 60, "CA": 60, "PA": 60, "Estado": 140}
        
        for c in cols:
            t.heading(c, text=c)
            t.column(c, width=config_p[c], anchor="center")
        t.column("Nombre", anchor="w")
        
        for j in equipo.plantilla:
            estado_txt = "Disponible"
            if j.lesionado: estado_txt = f"🚑 {j.dias_lesion}j"
            elif j.sancionado: estado_txt = "🟥 Sancionado"
            
            t.insert("", "end", values=(j.nombre, j.posicion, j.edad, j.ca, j.pa, estado_txt))
        
        t.pack(expand=True, fill="both", padx=15, pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = FMGui(root)
    root.mainloop()