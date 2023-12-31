import tkinter as tk
import random

class Habitacion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = random.choice(["Limpio", "Sucio"])
        self.bolitas = 3 if self.estado == "Sucio" else 0

    def ensuciar(self):
        self.estado = "Sucio"
        self.bolitas = 3
        
    def limpiar(self):
        if self.bolitas > 0:
            self.bolitas -= 1
        if self.bolitas == 0:
            self.estado = "Limpio"


class Aspiradora:
    def __init__(self, habitaciones):
        self.posicion = habitaciones[0]
        self.habitaciones = habitaciones
        
    def actuar(self):
        if self.posicion.estado == "Sucio":
            self.posicion.limpiar()
        else:
            # Cambiar a la otra habitación
            self.posicion = self.habitaciones[1] if self.posicion == self.habitaciones[0] else self.habitaciones[0]


class App:
    def __init__(self, root, aspiradora, habitacion_A, habitacion_B):
        self.root = root
        self.aspiradora = aspiradora
        self.habitaciones = [habitacion_A, habitacion_B]
        
        # Cargar la imagen de la aspiradora y redimensionarla
        img = tk.PhotoImage(file='aspiradora.png')
        self.aspiradora_img = img.subsample(6, 6)  # Cambia el valor para ajustar el tamaño
        
        # Título
        root.title("Aspiradora Inteligente")
        
        # Habitaciones con LabelFrame y Canvas para representar la aspiradora
        self.frames_habitaciones = {
            "A": tk.LabelFrame(root, text=f"Habitación A", width=200, height=200),
            "B": tk.LabelFrame(root, text=f"Habitación B", width=200, height=200)
        }

        self.canvas_habitaciones = {
            "A": tk.Canvas(self.frames_habitaciones["A"], width=190, height=180, bg="white"),
            "B": tk.Canvas(self.frames_habitaciones["B"], width=190, height=180, bg="white")
        }

        for nombre in self.frames_habitaciones:
            frame = self.frames_habitaciones[nombre]
            canvas = self.canvas_habitaciones[nombre]
            frame.pack(padx=10, pady=10, side=tk.LEFT)
            canvas.pack(padx=5, pady=5)
            
        # Botones para ensuciar
        self.buttons = {
            "A": tk.Button(root, text="Ensuciar A", command=lambda: self.ensuciar(habitacion_A)),
            "B": tk.Button(root, text="Ensuciar B", command=lambda: self.ensuciar(habitacion_B))
        }
        
        for button in self.buttons.values():
            button.pack(padx=10, pady=5)
        
        # Iniciar el ciclo de actuación automática de la aspiradora
        self.actuar_automaticamente()
        
    def ensuciar(self, habitacion):
        habitacion.ensuciar()
        self.actualizar_gui()
        
    def actuar_aspiradora(self):
        self.aspiradora.actuar()
        self.actualizar_gui()

    def actuar_automaticamente(self):
        self.actuar_aspiradora()
        self.root.after(2000, self.actuar_automaticamente)  # Actuar cada 2 segundos

    def actualizar_gui(self):
        for habitacion in self.habitaciones:
            canvas = self.canvas_habitaciones[habitacion.nombre]
                
            # Limpiar el canvas
            canvas.delete("all")
                
            # Dibujar la aspiradora si está en la habitación
            if habitacion == self.aspiradora.posicion:
                canvas.create_image(95, 95, image=self.aspiradora_img)  # Representar aspiradora como la imagen

            # Dibujar bolitas en forma de triángulo si la habitación está sucia
            bolitas_coords = [
                (95, 145),
                (85, 165),
                (105, 165)
            ]
            
            for i in range(habitacion.bolitas):
                x, y = bolitas_coords[i]
                size = 10
                canvas.create_oval(x, y, x+size, y+size, fill="brown")

# Crear las habitaciones y la aspiradora
habitacion_A = Habitacion("A")
habitacion_B = Habitacion("B")
aspiradora = Aspiradora([habitacion_A, habitacion_B])

root = tk.Tk()
app = App(root, aspiradora, habitacion_A, habitacion_B)
root.mainloop()
