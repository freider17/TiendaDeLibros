import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

def ingresar_libro():
    # Solicitar los datos del libro al usuario mediante cuadros de diálogo
    nombre = simpledialog.askstring("Nuevo libro", "Ingrese el nombre del libro:")
    if nombre is None:  # Si el usuario cierra el cuadro de diálogo o presiona "Cancelar"
        return

    id_libro = simpledialog.askinteger("Nuevo libro", "Ingrese el ID del libro:")
    if id_libro is None:
        return

    cantidad = simpledialog.askinteger("Nuevo libro", "Ingrese la cantidad de libros:")
    if cantidad is None:
        return

    precio_unidad = simpledialog.askfloat("Nuevo libro", "Ingrese el precio por unidad:")
    if precio_unidad is None:
        return

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect("libreria.db")  # Reemplaza "nombre_de_tu_base_de_datos.db" con el nombre de tu base de datos
    c = conn.cursor()

def actualizar_libro():
    # Solicitar el ID del libro a actualizar
    id_libro = simpledialog.askinteger("Actualizar libro", "Ingrese el ID del libro que desea actualizar:")
    if id_libro is None:
        return

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect("libreria.db")  # Reemplaza "libreria.db" con el nombre de tu base de datos
    c = conn.cursor()

    # Buscar el libro en la base de datos por su ID
    c.execute("SELECT nombre, cantidad, precio_unidad FROM libros WHERE id=?", (id_libro,))
    libro = c.fetchone()

    if not libro:
        messagebox.showerror("Error", "El libro con el ID ingresado no existe.")
        conn.close()
        return

    # Mostrar cuadros de diálogo para actualizar los datos del libro
    nuevo_nombre = simpledialog.askstring("Actualizar libro", "Ingrese el nuevo nombre del libro:", initialvalue=libro[0])
    if nuevo_nombre is None:
        conn.close()
        return

    nueva_cantidad = simpledialog.askinteger("Actualizar libro", "Ingrese la nueva cantidad de libros:", initialvalue=libro[1])
    if nueva_cantidad is None:
        conn.close()
        return

    nuevo_precio_unidad = simpledialog.askfloat("Actualizar libro", "Ingrese el nuevo precio por unidad:", initialvalue=libro[2])
    if nuevo_precio_unidad is None:
        conn.close()
        return

    # Actualizar los datos del libro en la base de datos
    try:
        c.execute("UPDATE libros SET nombre=?, cantidad=?, precio_unidad=? WHERE id=?", (nuevo_nombre, nueva_cantidad, nuevo_precio_unidad, id_libro))
        conn.commit()
        messagebox.showinfo("Éxito", "Libro actualizado correctamente.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al actualizar el libro: {e}")
    finally:
        conn.close()

def buscar_libro_por_id():
    # Solicitar el ID del libro a buscar
    id_libro = simpledialog.askinteger("Buscar libro", "Ingrese el ID del libro que desea buscar:")
    if id_libro is None:
        return

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect("libreria.db")  # Reemplaza "libreria.db" con el nombre de tu base de datos
    c = conn.cursor()

    # Buscar el libro en la base de datos por su ID
    c.execute("SELECT id, nombre, cantidad, precio_unidad FROM libros WHERE id=?", (id_libro,))
    libro = c.fetchone()

    if not libro:
        messagebox.showerror("Error", "El libro con el ID ingresado no existe.")
        conn.close()
        return

    # Mostrar información del libro encontrado
    messagebox.showinfo("Información del libro", f"ID: {libro[0]}\nNombre: {libro[1]}\nCantidad: {libro[2]}\nPrecio por unidad: {libro[3]}")

    conn.close()

def eliminar_libro_por_id():
    # Solicitar el ID del libro a eliminar
    id_libro = simpledialog.askinteger("Eliminar libro", "Ingrese el ID del libro que desea eliminar:")
    if id_libro is None:
        return

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect("libreria.db")  # Reemplaza "libreria.db" con el nombre de tu base de datos
    c = conn.cursor()

    # Buscar el libro en la base de datos por su ID
    c.execute("SELECT id, nombre, cantidad, precio_unidad FROM libros WHERE id=?", (id_libro,))
    libro = c.fetchone()

    if not libro:
        messagebox.showerror("Error", "El libro con el ID ingresado no existe.")
        conn.close()
        return

    # Mostrar ventana de confirmación para eliminar el libro
    confirmacion = messagebox.askyesno("Confirmación", f"¿Estás seguro de eliminar el libro con ID {id_libro}?\nNombre: {libro[1]}")
    if not confirmacion:
        conn.close()
        return

    # Eliminar el libro de la base de datos
    try:
        c.execute("DELETE FROM libros WHERE id=?", (id_libro,))
        conn.commit()
        messagebox.showinfo("Éxito", "Libro eliminado correctamente.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al eliminar el libro: {e}")
    finally:
        conn.close()

def ver_todos_los_libros():
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect("libreria.db")  # Reemplaza "libreria.db" con el nombre de tu base de datos
    c = conn.cursor()

    # Obtener todos los libros de la base de datos
    c.execute("SELECT id, nombre, cantidad, precio_unidad FROM libros")
    libros = c.fetchall()

    if not libros:
        messagebox.showinfo("Información", "No hay libros en la base de datos.")
        conn.close()
        return

    # Crear una ventana para mostrar la lista de libros
    ventana_lista_libros = tk.Toplevel()
    ventana_lista_libros.title("Lista de Libros")
    ventana_lista_libros.geometry("400x300")

    # Crear una etiqueta para mostrar la lista de libros en la ventana
    lista_libros_label = tk.Label(ventana_lista_libros, text="Lista de Libros", font=("Arial", 16))
    lista_libros_label.pack(pady=10)

    lista_texto = tk.Text(ventana_lista_libros, height=15, width=40)
    lista_texto.pack()

    # Mostrar la lista de libros en la ventana
    for libro in libros:
        lista_texto.insert(tk.END, f"ID: {libro[0]}\nNombre: {libro[1]}\nCantidad: {libro[2]}\nPrecio por unidad: {libro[3]}\n\n")

    # Deshabilitar la edición del texto para que el usuario no pueda modificar la lista
    lista_texto.config(state=tk.DISABLED)

    conn.close()
