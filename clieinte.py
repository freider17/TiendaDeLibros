# db_operations.py
import sqlite3

def conectar_bd(db_name):
    conexion = sqlite3.connect(db_name)
    cursor = conexion.cursor()
    return conexion, cursor

def desconectar_bd(conexion, cursor):
    cursor.close()
    conexion.close()

def create_table_clientes(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY,
                        nombre TEXT
                    )""")

def insert_cliente(cursor, id, nombre):
    sentencia = "INSERT INTO clientes (id, nombre) VALUES (?, ?)"
    parametros = (id, nombre)
    cursor.execute(sentencia, parametros)

def update_cliente(cursor, nuevo_id, nuevo_nombre, id_actualizar):
    sentencia = "UPDATE clientes SET id=?, nombre=? WHERE id=?"
    parametros = (nuevo_id, nuevo_nombre, id_actualizar)
    cursor.execute(sentencia, parametros)

def delete_cliente(cursor, id):
    sentencia = "DELETE FROM clientes WHERE id=?"
    cursor.execute(sentencia, (id,))

def is_valid_id(id_input):
    try:
        return int(id_input) >= 0
    except ValueError:
        return False

def is_valid_cliente_id(cursor, id):
    cursor.execute("SELECT id FROM clientes WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    return resultado is not None

def is_valid_name(name):
    return len(name.strip()) > 0

# db_operations.py
import sqlite3

# (Las funciones de conectar_bd, desconectar_bd, create_table_clientes,
# insert_cliente, update_cliente, delete_cliente, is_valid_id y is_valid_name se mantienen igual)

def list_clients(cursor):
    """
    Obtiene todos los clientes de la tabla 'clientes' y los muestra en la consola.

    :param cursor: Objeto cursor utilizado para interactuar con la base de datos.
    """
    cursor.execute("SELECT id, nombre FROM clientes")
    clientes = cursor.fetchall()
    if not clientes:
        print("No se encontró ningún cliente en la base de datos.")
    else:
        print("--- Lista de Clientes ---")
        for id, nombre in clientes:
            print(f"ID: {id}, Nombre del cliente: {nombre}")
        print()

def search_client(cursor, cliente_id):
    """
    Busca un cliente en la tabla 'clientes' según su ID y muestra la información en la consola.

    :param cursor: Objeto cursor utilizado para interactuar con la base de datos.
    :param cliente_id: ID del cliente a buscar.
    """
    cursor.execute("SELECT id, nombre FROM clientes WHERE id=?", (cliente_id,))
    cliente = cursor.fetchone()
    if cliente is None:
        print("No se encontró ningún cliente asociado en la base de datos.")
    else:
        print(f"ID: {cliente[0]}, Nombre del cliente: {cliente[1]}")
    print()



