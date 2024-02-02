import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from PIL import Image, ImageTk

def do_nothing():
    messagebox.showinfo("Placeholder", "Esta opción aún no está implementada.")

def show_client_menu():
    client_menu.tk_popup(root.winfo_pointerx(), root.winfo_pointery())

def show_library_menu():
    library_menu.tk_popup(root.winfo_pointerx(), root.winfo_pointery())

def show_sales_menu():
    sales_menu.tk_popup(root.winfo_pointerx(), root.winfo_pointery())

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

def buscar_cliente_por_nombre(nombre_cliente):
    conn = sqlite3.connect("clientes.db")
    c = conn.cursor()
    c.execute("SELECT * FROM clientes WHERE nombre=?", (nombre_cliente,))
    cliente = c.fetchone()
    conn.close()
    return cliente

def buscar_cliente_por_codigo(codigo_cliente):
    conn = sqlite3.connect("clientes.db")
    c = conn.cursor()
    c.execute("SELECT * FROM clientes WHERE id=?", (codigo_cliente,))
    cliente = c.fetchone()
    conn.close()
    return cliente

def buscar_cliente():
    # Preguntar al usuario si desea buscar por nombre o por código
    opcion = simpledialog.askstring("Buscar cliente", "¿Deseas buscar por nombre o por código? (nombre/codigo):")
    
    if opcion and opcion.lower() in ["nombre", "codigo"]:
        if opcion.lower() == "nombre":
            nombre_cliente = simpledialog.askstring("Buscar cliente", "Ingresa el nombre del cliente:")
            if nombre_cliente:
                cliente = buscar_cliente_por_nombre(nombre_cliente)
                if cliente:
                    messagebox.showinfo("Cliente encontrado", f"Cliente encontrado en la posición {cliente[0]}. Nombre: {cliente[1]}.")
                else:
                    messagebox.showwarning("Cliente no encontrado", f"No se encontró un cliente con el nombre '{nombre_cliente}'.")
            else:
                messagebox.showwarning("Error", "Por favor, ingresa un nombre válido.")
        else:  # Buscar por código
            codigo_cliente = simpledialog.askinteger("Buscar cliente", "Ingresa el código del cliente:")
            if codigo_cliente:
                cliente = buscar_cliente_por_codigo(codigo_cliente)
                if cliente:
                    messagebox.showinfo("Cliente encontrado", f"Cliente encontrado en la posición {cliente[0]}. Nombre: {cliente[1]}.")
                else:
                    messagebox.showwarning("Cliente no encontrado", f"No se encontró un cliente con el código '{codigo_cliente}'.")
            else:
                messagebox.showwarning("Error", "Por favor, ingresa un código válido.")
    else:
        messagebox.showwarning("Error", "Opción inválida. Debes ingresar 'nombre' o 'codigo'.")

def agregar_cliente():
    # Crea un cuadro de diálogo para ingresar el nombre del cliente
    cliente_nombre = simpledialog.askstring("Agregar cliente", "Nombre del cliente:")
    if cliente_nombre:
        # Guardar el cliente en la base de datos SQLite
        conn = sqlite3.connect("clientes.db")  # Conectar a la base de datos (creará si no existe)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT)''')
        c.execute("INSERT INTO clientes (nombre) VALUES (?)", (cliente_nombre,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Cliente agregado", f"El cliente {cliente_nombre} ha sido agregado exitosamente.")

def actualizar_cliente():
    # Crea un cuadro de diálogo para ingresar el nombre del cliente a actualizar
    nombre_cliente = simpledialog.askstring("Actualizar cliente", "Nombre del cliente a actualizar:")
    if nombre_cliente:
        cliente = buscar_cliente_por_nombre(nombre_cliente)
        if cliente:
            # Muestra un cuadro de diálogo para ingresar los nuevos datos
            nuevo_nombre = simpledialog.askstring("Actualizar cliente", "Nuevo nombre del cliente:", initialvalue=cliente[1])
            if nuevo_nombre:
                # Actualiza el cliente en la base de datos
                conn = sqlite3.connect("clientes.db")
                c = conn.cursor()
                c.execute("UPDATE clientes SET nombre=? WHERE id=?", (nuevo_nombre, cliente[0]))
                conn.commit()
                conn.close()
                messagebox.showinfo("Cliente actualizado", f"El cliente ha sido actualizado exitosamente.")
            else:
                messagebox.showwarning("Error", "Por favor, ingresa un nuevo nombre válido.")
        else:
            messagebox.showwarning("Error", f"No se encontró un cliente con el nombre '{nombre_cliente}'.")

# Configuración básica de la ventana
root = tk.Tk()
root.title("LIBRE SOY")
root.geometry("400x500")  # Aumentamos la altura para dejar espacio al cuadro de texto

# Mensaje de bienvenida con un fondo de color diferente
welcome_frame = tk.Frame(root, bg="pink")  # Color de fondo del cuadro del mensaje
welcome_frame.pack(pady=10)

welcome_label = tk.Label(welcome_frame, text="¡Bienvenido a LIBRE SOY!", font=("Arial", 20), padx=10, pady=10)
welcome_label.pack()

# Color de fondo en la ventana
root.configure(bg="pink")

# Cargar la imagen (mismo código que antes)
image_path = "foto.png"
try:
    image = Image.open(image_path)
    image = image.resize((200, 200))
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=photo)
    image_label.pack(pady=10)
except FileNotFoundError:
    print("Error: No se pudo encontrar la imagen.")

# Cuadro de texto para dejar una opinión
opinion_label = tk.Label(root, text="Deja tu opinión sobre la experiencia:", font=("Arial", 12), padx=10, pady=5)
opinion_label.pack()

opinion_text = tk.Text(root, height=5, width=40)
opinion_text.pack(padx=10, pady=5)

# Botón para guardar la opinión
save_button = tk.Button(root, text="Guardar Opinión", command=save_opinion)
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
client_menu.add_separator()
client_menu.add_command(label="Eliminar cliente", command=do_nothing)

# Menú de "Librería"
library_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Librería", menu=library_menu)
library_menu.add_command(label="Agregar libro", command=do_nothing)
library_menu.add_command(label="Actualizar libro", command=do_nothing)
library_menu.add_command(label="Buscar libro", command=do_nothing)
library_menu.add_separator()
library_menu.add_command(label="Eliminar libro", command=do_nothing)

# Menú de "Ventas"
sales_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Ventas", menu=sales_menu)
sales_menu.add_command(label="Realizar venta", command=do_nothing)
sales_menu.add_command(label="Actualizar venta", command=do_nothing)
sales_menu.add_command(label="Buscar venta", command=do_nothing)
sales_menu.add_command(label="Eliminar ventas", command=do_nothing)
sales_menu.add_separator()

root.mainloop()
