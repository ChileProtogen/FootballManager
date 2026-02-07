class Equipo:
    def __init__(self, nombre, ciudad, presupuesto, reputacion):
        self.nombre = nombre
        self.ciudad = ciudad
        self.presupuesto = presupuesto
        self.reputacion = reputacion
        self.plantilla = []
        self.entrenador = None

    def __repr__(self):
        return f"{self.nombre} ({self.ciudad}) - Rep: {self.reputacion}"