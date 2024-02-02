import os
import tkinter as tk
from tkinter import messagebox, simpledialog

import sqlite3
from ig_cliente import * 
from ig_libros import *
from ventas import *
from estadisticas import *

def do_nothing():
    messagebox.showinfo("Placeholder", "Esta opción aún no está implementada.")

def save_opinion():
    opinion = opinion_text.get("1.0", tk.END).strip()
    if opinion != "":
        # Guardar la opinión en la base de datos SQLite
        conn = sqlite3.connect("opinions.db")  # Conectar a la base de datos (creará si no existe)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS opinions (id INTEGER PRIMARY KEY AUTOINCREMENT, opinion_text TEXT)''')
        c.execute("INSERT INTO opinions (opinion_text) VALUES (?)", (opinion,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Gracias", "¡Gracias por tu opinión!")
    else:
        messagebox.showwarning("Error", "Por favor, ingresa una opinión válida.")

root = tk.Tk()
root.title("LIBRE SOY")
root.geometry("800x800")  # Aumentamos la altura para dejar espacio al cuadro de texto

# Mensaje de bienvenida con un fondo de color diferente
welcome_frame = tk.Frame(root, bg="lavender")  # Color de fondo del cuadro del mensaje
welcome_frame.pack(pady=10)

welcome_label = tk.Label(welcome_frame, text="¡Bienvenido a LIBRE SOY!", font=("Arial", 20), bg='lavender', padx=10, pady=10)
welcome_label.pack()

root.configure(bg="lavender")

script_directory = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_directory, "images.png")  # Reemplaza "nombre_de_la_imagen.jpg" con el nombre de tu imagen



    
# Cuadro de texto para dejar una opinión
opinion_label = tk.Label(root, text="Deja tu opinión sobre la experiencia:",  font=("Arial", 12), bg='lavender', padx=10, pady=5)
opinion_label.pack()

opinion_text = tk.Text(root, height=5, width=40,bg='aliceblue')
opinion_text.pack(padx=5, pady=5,)

# Botón para guardar la opinión
save_button = tk.Button(root, text="Guardar Opinión",bg='lavender', command=save_opinion)
save_button.pack(pady=10)

# Menú principal
main_menu = tk.Menu(root)
root.config(menu=main_menu)

# Menú de "Clientes"
client_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Clientes", menu=client_menu)
client_menu.add_command(label="Agregar cliente", command=agregar_cliente)
client_menu.add_command(label="Actualizar cliente", command=actualizar_cliente)
client_menu.add_command(label="Buscar cliente", command=buscar_cliente)
client_menu.add_command(label="Eliminar cliente", command=eliminar_cliente)
client_menu.add_command(label="listar cliente", command=listar_clientes)
                        
# Menú de "Librería"
library_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Librería", menu=library_menu)
library_menu.add_command(label="Agregar libro", command=ingresar_libro)
library_menu.add_command(label="Actualizar libro", command=actualizar_libro)
library_menu.add_command(label="Buscar libro", command=buscar_libro_por_id)
library_menu.add_command(label="Eliminar libro", command=eliminar_libro_por_id)
library_menu.add_command(label="listar libros", command=ver_todos_los_libros)

# Menú de "Ventas"
sales_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Ventas", menu=sales_menu)
sales_menu.add_command(label="Realizar venta", command=realizar_venta)
sales_menu.add_command(label="Actualizar venta", command=actualizar_venta)
sales_menu.add_command(label="Buscar venta", command=buscar_venta)
sales_menu.add_command(label="Eliminar ventas", command=do_nothing)
sales_menu.add_command(label="listar ventas", command=lista_ventas)


stats_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Estadísticas", menu=stats_menu)
stats_menu.add_command(label="Ventas totales por libro", command=obtener_ventas_totales_por_codigo_libro)
stats_menu.add_command(label="Libros mayor y menor vendido", command=mostrar_libros_mas_y_menos_vendido)
stats_menu.add_command(label="Ventas totales de librería", command=calcular_venta_total_libreria)
stats_menu.add_command(label="Volumen de compra", command=volumen_compra)

root.mainloop()
