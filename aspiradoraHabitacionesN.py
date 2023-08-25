import tkinter as tk
import random
from tkinter import simpledialog, messagebox

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
            # Cambiar a la siguiente habitación
            index_actual = self.habitaciones.index(self.posicion)
            siguiente_index = (index_actual + 1) % len(self.habitaciones)
            self.posicion = self.habitaciones[siguiente_index]

class App:
    def __init__(self, root, aspiradora, habitaciones, aspiradora_img):
        self.root = root
        self.aspiradora = aspiradora
        self.habitaciones = habitaciones
        self.aspiradora_img = aspiradora_img
        
        # Título
        root.title("Aspiradora Inteligente")
        
        # Habitaciones con LabelFrame y Canvas para representar la aspiradora
        self.frames_habitaciones = {}
        self.canvas_habitaciones = {}
        for habitacion in habitaciones:
            frame = tk.LabelFrame(root, text=f"Habitación {habitacion.nombre}", width=200, height=200)
            canvas = tk.Canvas(frame, width=190, height=180, bg="white")
            self.frames_habitaciones[habitacion.nombre] = frame
            self.canvas_habitaciones[habitacion.nombre] = canvas
            frame.pack(padx=10, pady=10, side=tk.LEFT)
            canvas.pack(padx=5, pady=5)
            
            # Botones para ensuciar
            button = tk.Button(root, text=f"Ensuciar {habitacion.nombre}", command=lambda h=habitacion: self.ensuciar(h))
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

# Preguntar al usuario cuántas habitaciones desea
root_temp = tk.Tk()
root_temp.withdraw()  # Esconder la ventana raíz principal
num_habitaciones = simpledialog.askinteger("Configuración", "¿Cuántas habitaciones deseas?", minvalue=2, maxvalue=10)

if num_habitaciones is None:
    messagebox.showinfo("Info", "Operación cancelada por el usuario.")
    exit()

# Crear las habitaciones y la aspiradora dinámicamente
habitaciones = [Habitacion(str(i+1)) for i in range(num_habitaciones)]
aspiradora = Aspiradora(habitaciones)

# Cargar la imagen de la aspiradora y redimensionarla a nivel global
aspiradora_img = tk.PhotoImage(file='aspiradora.png').subsample(6, 6)

root = tk.Tk()
app = App(root, aspiradora, habitaciones, aspiradora_img)
root.mainloop()
