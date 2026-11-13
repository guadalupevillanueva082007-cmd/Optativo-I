import psycopg2

class GestorPedidos:
    """Clase que agrupa todas las operaciones sobre la tabla pedidos y consultas auxiliares."""

    def __init__(self, host, port, dbname, user, password):
        self.conexion = psycopg2.connect(
            host=host, port=port, dbname=dbname,
            user=user, password=password
        )
        self.cursor = self.conexion.cursor()
        print("Conexion exitosa a la base de datos (Pedidos)")

    # -- Método auxiliar para mostrar clientes disponibles --
    def mostrar_clientes_disponibles(self):
        self.cursor.execute("SELECT id_cliente, nombre FROM clientes ORDER BY id_cliente")
        filas = self.cursor.fetchall()
        if not filas:
            print("No hay clientes registrados en la base de datos.")
            return False
        print("\n--- CLIENTES DISPONIBLES ---")
        print(f"{'ID':<6}{'Nombre':<20}")
        print("-" * 26)
        for f in filas:
            print(f"{f[0]:<6}{f[1]:<20}")
        return True

    # -- Método auxiliar para mostrar productos disponibles --
    def mostrar_productos_disponibles(self):
        self.cursor.execute("SELECT id_producto, nombre, precio, stock FROM productos ORDER BY id_producto")
        filas = self.cursor.fetchall()
        if not filas:
            print("No hay productos registrados en la base de datos.")
            return False
        print("\n--- PRODUCTOS DISPONIBLES ---")
        print(f"{'ID':<6}{'Nombre':<20}{'Precio':<12}{'Stock':<8}")
        print("-" * 46)
        for f in filas:
            print(f"{f[0]:<6}{f[1]:<20}{str(f[2]):<12}{f[3]:<8}")
        return True

    # -- CREATE: insertar un pedido nuevo mostrando las opciones antes --
    def crear(self):
        print("\n--- ASISTENTE PARA NUEVO PEDIDO ---")
        # Mostramos clientes y productos para que elijas visualmente
        if not self.mostrar_clientes_disponibles() or not self.mostrar_productos_disponibles():
            print("⚠️ Necesitas tener al menos un cliente y un producto registrados para crear un pedido.")
            return

        print("\n")
        id_cliente = input("Ingrese el ID del Cliente elegido: ")
        id_producto = input("Ingrese el ID del Producto elegido: ")
        cantidad = int(input("Ingrese la cantidad: "))

        try:
            self.cursor.execute(
                "INSERT INTO pedidos (id_cliente, id_producto, cantidad, fecha) VALUES (%s, %s, %s, CURRENT_DATE)",
                (id_cliente, id_producto, cantidad)
            )
            self.conexion.commit()
            print("✅ Pedido insertado correctamente.")
        except psycopg2.Error as e:
            self.conexion.rollback()
            print("❌ No se pudo insertar el pedido (el ID de cliente o producto no existe):", e)

    # -- READ: listar todos los pedidos --
    def listar(self):
        self.cursor.execute(
            "SELECT id_pedido, id_cliente, id_producto, cantidad, fecha FROM pedidos ORDER BY id_pedido"
        )
        filas = self.cursor.fetchall()
        if not filas:
            print("No hay pedidos cargados.")
            return
        print(f"\n{'ID Pedido':<10}{'ID Cliente':<12}{'ID Producto':<13}{'Cantidad':<10}{'Fecha':<12}")
        print("-" * 57)
        for f in filas:
            print(f"{f[0]:<10}{f[1]:<12}{f[2]:<13}{f[3]:<10}{str(f[4]):<12}")

    # -- UPDATE: modificar la cantidad de un pedido --
    def modificar(self, id_pedido, nueva_cantidad):
        self.cursor.execute(
            "UPDATE pedidos SET cantidad = %s WHERE id_pedido = %s",
            (nueva_cantidad, id_pedido)
        )
        self.conexion.commit()
        if self.cursor.rowcount > 0:
            print(f"✅ Pedido actualizado ({self.cursor.rowcount} fila modificada)")
        else:
            print("❌ No se encontró ningún pedido con ese ID.")

    # -- DELETE: borrar un pedido --
    def borrar(self, id_pedido):
        try:
            self.cursor.execute(
                "DELETE FROM pedidos WHERE id_pedido = %s",
                (id_pedido,)
            )
            self.conexion.commit()
            if self.cursor.rowcount > 0:
                print(f"✅ Pedido borrado ({self.cursor.rowcount} fila eliminada)")
            else:
                print("❌ No se encontró ningún pedido con ese ID.")
        except psycopg2.Error as e:
            self.conexion.rollback()
            print("❌ No se pudo borrar el pedido:", e)

    # -- Cerrar la conexion --
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
        print("Conexión cerrada. ¡Hasta luego!")


def mostrar_menu_pedidos():
    print("\n===== GESTION DE PEDIDOS =====")
    print("1. Agregar pedido (Muestra clientes y productos)")
    print("2. Listar pedidos")
    print("3. Modificar cantidad de un pedido")
    print("4. Borrar pedido")
    print("5. Salir")
    print("================================")


def main():
    gestor = GestorPedidos(
        host="localhost",
        port=5432,
        dbname="comercio",
        user="postgres",
        password="G080607"
    )

    while True:
        mostrar_menu_pedidos()
        opcion = input("Elija una opción (1-5): ")

        if opcion == "1":
            gestor.crear()

        elif opcion == "2":
            gestor.listar()

        elif opcion == "3":
            id_pedido = input("ID del pedido a modificar: ")
            nueva_cantidad = int(input("Nueva cantidad: "))
            gestor.modificar(id_pedido, nueva_cantidad)

        elif opcion == "4":
            id_pedido = input("ID del pedido a borrar: ")
            gestor.borrar(id_pedido)

        elif opcion == "5":
            gestor.cerrar()
            break

        else:
            print("⚠️ Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()