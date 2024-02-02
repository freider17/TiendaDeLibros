from sqlLibreria import conectar_bd, desconectar_bd
def ingresar_libro():
    while True:
        conexion, cursor = conectar_bd("Libreria.db")
        print("Para volver al menu, ingrese 0")

        try:
            id = int(input("Ingrese el ID del libro: "))
            if id == '0':
                break
        except ValueError:
            print("Error: Debes ingresar un valor numérico para el ID del libro.")
            continue

        # Verificar si el ID ya está registrado
        cursor.execute("SELECT COUNT(*) FROM libros WHERE id = ?", (id,))
        resultado = cursor.fetchone()
        if resultado[0] > 0:
            print("El ID ingresado ya está registrado en la base de datos , ingrese un ID diferente.")
            continue

        nombre_Libro = input("Ingrese el nombre del libro: ")
        if nombre_Libro == '0':
            break

        while True:
            try:
                valor = int(input("Ingrese el valor del libro: "))
                break
            except ValueError:
                print("Error: Debes ingresar un valor numérico.")

        cantidad = int(input("Ingrese la cantidad de libros: "))

        nuevo_libro = [id, nombre_Libro, valor, cantidad]
        print()
        sentencia = """INSERT INTO libros(id, nombre_libro, valor, cantidad)
                    VALUES (?, ?, ?, ?)"""
        cursor.execute(sentencia, nuevo_libro)
        conexion.commit()
        desconectar_bd(conexion, cursor)
        print("Libro registrado satisfactoriamente")




def lista_libros():
    conexion, cursor = conectar_bd("Libreria.db")

    print("===Lista de Libros===")

    sentencia = """SELECT id, nombre_libro, CAST(valor AS INTEGER), cantidad
                   FROM libros"""

    cursor.execute(sentencia)

    libros = cursor.fetchall()
    for id, nombre_libro, valor, cantidad in libros:
        print(f"ID: {id}, Nombre del libro: {nombre_libro}, valor: {valor}, cantidad: {cantidad}")
        print()

    desconectar_bd(conexion, cursor)


def actualizar_libro():
    conexion, cursor = conectar_bd("Libreria.db")

    sentencia = """SELECT id, nombre_libro, valor, cantidad
                   FROM libros"""
    cursor.execute(sentencia)
    libros = cursor.fetchall()

    for id, nombre_libro, valor, cantidad in libros:
        print(f"ID: {id}, Nombre del libro: {nombre_libro}, valor: {int(valor)}, cantidad: {cantidad}")
        print()

    while True:
        try:
            id_actualizar = int(input("Ingrese el ID del libro a actualizar 0 para volver al menú: "))
            if id_actualizar == 0:
                break
        except ValueError:
            print("Error: Ingrese un valor númerico para el ID.")

        # Verificar si el libro tiene una venta asociada
        sentencia = """SELECT COUNT(*) FROM ventas WHERE id_libros=?"""
        cursor.execute(sentencia, (id_actualizar,))
        venta_asociada = cursor.fetchone()[0] > 0

        if venta_asociada:
            print("Error: No se puede actualizar el libro porque tiene una venta asociada.")
        else:
            while True:
                try:
                    nuevo_id = int(input("Si desea, ingrese el nuevo ID para el libro 0 para volver al menú: "))
                    if nuevo_id == 0:
                        break
                except ValueError:
                    print("Error: Ingrese un valor entero válido para el nuevo ID.")

                nuevo_titulo = input("Ingrese el nuevo título del Libro (0 para salir): ")
                if nuevo_titulo == "0":
                    break

                while True:
                    try:
                        nuevo_valor = int(input("Ingrese el nuevo valor del Libro solo números enteros ,0 para volver al menú): "))
                        if nuevo_valor == 0:
                            break
                    except ValueError:
                        print("Error: Ingrese un valor entero válido para el valor del libro.")

                    nueva_cantidad = int(input("Ingrese la nueva cantidad de Libros 0 para volver al menú: "))
                    if nueva_cantidad == 0:
                        break

                    print()

                    sentencia = """UPDATE libros
                                   SET id=?, nombre_libro=?, valor=?, cantidad=?
                                   WHERE id=?"""

                    parametros = [nuevo_id, nuevo_titulo, nuevo_valor, nueva_cantidad, id_actualizar]
                    cursor.execute(sentencia, parametros)
                    conexion.commit()

                    # Mostrar solo el libro actualizado
                    sentencia = """SELECT id, nombre_libro, valor, cantidad
                                   FROM libros
                                   WHERE id=?"""
                    cursor.execute(sentencia, (id_actualizar,))
                    libro_actualizado = cursor.fetchone()

                    print(f"ID: {libro_actualizado[0]}, Nombre del libro: {libro_actualizado[1]}, valor: {int(libro_actualizado[2])}, cantidad: {libro_actualizado[3]}")
                    print()

                    break  # Salir del bucle interno y volver a solicitar el ID del libro

    desconectar_bd(conexion, cursor)


def eliminar_libro():
    conexion, cursor = conectar_bd("Libreria.db")

    # Mostrar lista de libros actual antes de eliminar
    sentencia = """SELECT * FROM libros"""
    cursor.execute(sentencia)
    libros = cursor.fetchall()
    for id, nombre_libro, valor, cantidad in libros:
        print(f"ID: {id}, Nombre del libro: {nombre_libro}, Valor: {valor}, Cantidad: {cantidad}")
        print()

    id = int(input("Ingrese ID del libro a eliminar: "))

    # Verificar si el libro tiene ventas asociadas
    sentencia_venta = """SELECT COUNT(*) FROM ventas WHERE id_libros = ?"""
    cursor.execute(sentencia_venta, [id])
    venta_asociada = cursor.fetchone()[0] > 0

    if venta_asociada:
        print("No es posible eliminar el libro porque tiene ventas asociadas.")
    else:
        confirmacion = input("¿Está seguro de que desea eliminar este libro? (s/n): ")
        if confirmacion.lower() == "s":
            sentencia = """DELETE FROM libros WHERE id = ?;"""
            parametros = [id]
            cursor.execute(sentencia, parametros)
            conexion.commit()

            if cursor.rowcount > 0:
                print(f"Libro {id} eliminado con éxito")
                print()

                # Mostrar libro eliminado
                sentencia = """SELECT * FROM libros WHERE id = ?"""
                cursor.execute(sentencia, [id])
                libro_eliminado = cursor.fetchone()

                if libro_eliminado:
                    id, nombre_libro, valor, cantidad = libro_eliminado
                    print(f"Libro eliminado:")
                    print(f"ID: {id}, Nombre del libro: {nombre_libro}, Valor: {valor}, Cantidad: {cantidad}")
                    print()
            else:
                print("No se encontró ningún libro con el ID proporcionado.")
        else:
            print("Operación de eliminación cancelada.")

    desconectar_bd(conexion, cursor)

def buscar_libro():
    conexion, cursor = conectar_bd("Libreria.db")

    print("---Buscar Libro---")
    criterio = input("(ID del libro): ")
    print()

    # Buscar por ID
    if criterio.isdigit():
        id = int(criterio)
        sentencia = """SELECT id, nombre_libro, valor, cantidad
                       FROM libros
                       WHERE id = ?"""
        cursor.execute(sentencia, (id,))
    # Buscar por nombre del libro

    libros = cursor.fetchall()

    if len(libros) > 0:
        print()
        for id, nombre_libro, valor, cantidad in libros:
            valor_entero = int(valor)  # Convertir el valor en entero
            print(f"ID: {id}, Nombre del libro: {nombre_libro}, Valor: {valor_entero}, Cantidad: {cantidad}")
            print()
    else:
        print("No se encontro un libro asociado en la base de datos.")

    desconectar_bd(conexion, cursor)


