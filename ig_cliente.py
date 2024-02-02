import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

# ... (código previo)

def agregar_cliente():
    # Obtener el nombre y el ID del cliente utilizando simpledialog
    nombre_cliente = simpledialog.askstring("Agregar cliente", "Ingrese el nombre del cliente:")
    if nombre_cliente:
        id_cliente = simpledialog.askinteger("Agregar cliente", "Ingrese el ID del cliente:")
        if id_cliente is not None:
            # Guardar los datos del cliente en la base de datos SQLite
            conn = sqlite3.connect("libreria.db")
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY, nombre TEXT)''')
            c.execute("INSERT INTO clientes (id, nombre) VALUES (?, ?)", (id_cliente, nombre_cliente))
            conn.commit()
            conn.close()
            messagebox.showinfo("Cliente agregado", f"Se ha agregado el cliente '{nombre_cliente}' con ID {id_cliente}.")
        else:
            messagebox.showwarning("Error", "Debe ingresar un ID válido.")
    else:
        messagebox.showwarning("Error", "Debe ingresar un nombre de cliente válido.")

def actualizar_cliente():
    # Obtener el ID del cliente a actualizar
    id_cliente = simpledialog.askinteger("Actualizar cliente", "Ingrese el ID del cliente a actualizar:")
    if id_cliente is not None:
        # Verificar si el cliente existe en la base de datos
        conn = sqlite3.connect("Libreria.db")
        c = conn.cursor()
        c.execute("SELECT nombre FROM clientes WHERE id=?", (id_cliente,))
        cliente_data = c.fetchone()

        if cliente_data is not None:
            # Obtener el nuevo nombre del cliente
            nuevo_nombre = simpledialog.askstring("Actualizar cliente", "Ingrese el nuevo nombre del cliente:")
            if nuevo_nombre:
                # Obtener el nuevo ID del cliente
                nuevo_id = simpledialog.askinteger("Actualizar cliente", "Ingrese el nuevo ID del cliente:")
                if nuevo_id is not None:
                    # Actualizar los datos del cliente en la base de datos SQLite
                    c.execute("UPDATE clientes SET nombre=?, id=? WHERE id=?", (nuevo_nombre, nuevo_id, id_cliente))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Cliente actualizado", f"Se ha actualizado el cliente '{nuevo_nombre}' con ID {nuevo_id}.")
                else:
                    messagebox.showwarning("Error", "Debe ingresar un ID válido.")
            else:
                messagebox.showwarning("Error", "Debe ingresar un nombre de cliente válido.")
        else:
            messagebox.showwarning("Error", "No se encontró un cliente con el ID proporcionado.")
    else:
        messagebox.showwarning("Error", "Debe ingresar un ID de cliente válido.")


def buscar_cliente():
    # Obtener el ID del cliente a buscar
    id_cliente = simpledialog.askinteger("Buscar cliente", "Ingrese el ID del cliente a buscar:")
    if id_cliente is not None:
        # Realizar la consulta SQL para obtener el nombre y la posición del cliente en la tabla
        conn = sqlite3.connect("libreria.db")
        c = conn.cursor()
        c.execute("SELECT nombre, ROW_NUMBER() OVER () FROM clientes WHERE id=?", (id_cliente,))
        cliente_data = c.fetchone()

        if cliente_data is not None:
            # Mostrar el nombre y la posición del cliente en un cuadro de mensaje
            nombre_cliente, posicion = cliente_data
            messagebox.showinfo("Cliente encontrado", f"El cliente con ID {id_cliente} se llama '{nombre_cliente}' y se encuentra en la columna {posicion} de la tabla.")
        else:
            messagebox.showwarning("Cliente no encontrado", f"No se encontró un cliente con el ID {id_cliente}.")
    else:
        messagebox.showwarning("Error", "Debe ingresar un ID de cliente válido.")

def eliminar_cliente():
    # Obtener el ID del cliente a eliminar
    id_cliente = simpledialog.askinteger("Eliminar cliente", "Ingrese el ID del cliente a eliminar:")
    if id_cliente is not None:
        # Verificar si el cliente existe en la base de datos
        conn = sqlite3.connect("libreria.db")
        c = conn.cursor()
        c.execute("SELECT nombre FROM clientes WHERE id=?", (id_cliente,))
        cliente_data = c.fetchone()

        if cliente_data is not None:
            # Mostrar una ventana de confirmación antes de eliminar al cliente
            confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de que quieres eliminar al cliente con ID {id_cliente}?")

            if confirmacion:
                # Eliminar al cliente de la base de datos
                c.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Cliente eliminado", f"Se ha eliminado al cliente con ID {id_cliente}.")
            else:
                messagebox.showinfo("Eliminación cancelada", "La eliminación del cliente ha sido cancelada.")
        else:
            messagebox.showwarning("Cliente no encontrado", f"No se encontró un cliente con el ID {id_cliente}.")
    else:
        messagebox.showwarning("Error", "Debe ingresar un ID de cliente válido.")

def listar_clientes():
    # Realizar la consulta SQL para obtener todos los clientes registrados
    conn = sqlite3.connect("libreria.db")
    c = conn.cursor()
    c.execute("SELECT id, nombre FROM clientes")
    clientes_data = c.fetchall()

    if clientes_data:
        # Crear un mensaje con los datos de los clientes
        mensaje = "Clientes registrados:\n"
        for cliente in clientes_data:
            id_cliente, nombre_cliente = cliente
            mensaje += f"ID: {id_cliente}, Nombre: {nombre_cliente}\n"

        # Mostrar los datos de los clientes en un cuadro de mensaje
        messagebox.showinfo("Clientes registrados", mensaje)
    else:
        messagebox.showinfo("Clientes registrados", "No hay clientes registrados en la base de datos.")

    conn.close()