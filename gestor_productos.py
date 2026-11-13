import psycopg2

class GestorProductos:
    """Clase que agrupa todas las operaciones sobre la tabla productos."""

    def __init__(self, host, port, dbname, user, password):
        self.conexion = psycopg2.connect(
            host=host, port=port, dbname=dbname,
            user=user, password=password
        )
        self.cursor = self.conexion.cursor()
        print("Conexion exitosa a la base de datos (Productos)")

    # -- CREATE: insertar un producto nuevo --
    def crear(self, nombre, precio, stock):
        try:
            self.cursor.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
                (nombre, precio, stock)
            )
            self.conexion.commit()
            print(f"Producto '{nombre}' insertado correctamente")
        except psycopg2.Error as e:
            self.conexion.rollback()
            print("No se pudo insertar el producto:", e)

    # -- READ: listar todos los productos --
    def listar(self):
        self.cursor.execute(
            "SELECT id_producto, nombre, precio, stock FROM productos ORDER BY id_producto"
        )
        filas = self.cursor.fetchall()
        if not filas:
            print("No hay productos cargados")
            return
        print(f"{'ID':<4}{'Nombre':<25}{'Precio':<15}{'Stock':<10}")
        print("-" * 54)
        for f in filas:
            print(f"{f[0]:<4}{f[1]:<25}{str(f[2]):<15}{f[3]:<10}")

    # -- UPDATE: modificar precio y stock de un producto --
    def modificar(self, id_producto, nuevo_precio, nuevo_stock):
        self.cursor.execute(
            "UPDATE productos SET precio = %s, stock = %s WHERE id_producto = %s",
            (nuevo_precio, nuevo_stock, id_producto)
        )
        self.conexion.commit()
        if self.cursor.rowcount > 0:
            print(f"Producto actualizado ({self.cursor.rowcount} fila modificada)")
        else:
            print("No se encontro ningun producto con ese id")

    # -- DELETE: borrar un producto --
    def borrar(self, id_producto):
        try:
            self.cursor.execute(
                "DELETE FROM productos WHERE id_producto = %s",
                (id_producto,)
            )
            self.conexion.commit()
            if self.cursor.rowcount > 0:
                print(f"Producto borrado ({self.cursor.rowcount} fila eliminada)")
            else:
                print("No se encontro ningun producto con ese id")
        except psycopg2.Error as e:
            self.conexion.rollback()
            print("No se pudo borrar el producto: tiene pedidos asociados.")

    # -- Cerrar la conexion --
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
        print("Conexion cerrada.")

def mostrar_menu_productos():
    print("\n===== GESTION DE PRODUCTOS =====")
    print("1. Agregar producto")
    print("2. Listar productos")
    print("3. Modificar precio y stock de un producto")
    print("4. Borrar producto")
    print("5. Salir")
    print("================================")

def main():
    gestor = GestorProductos(
        host="localhost",
        port=5432,
        dbname="comercio",
        user="postgres",
        password="G080607"
    )

    while True:
        mostrar_menu_productos()
        opcion = input("Elija una opcion (1-5): ")

        if opcion == "1":
            nombre = input("Nombre del producto: ")
            precio = float(input("Precio: "))
            stock = int(input("Stock: "))
            gestor.crear(nombre, precio, stock)

        elif opcion == "2":
            gestor.listar()

        elif opcion == "3":
            id_producto = input("Id del producto a modificar: ")
            nuevo_precio = float(input("Nuevo precio: "))
            nuevo_stock = int(input("Nuevo stock: "))
            gestor.modificar(id_producto, nuevo_precio, nuevo_stock)

        elif opcion == "4":
            id_producto = input("Id del producto a borrar: ")
            gestor.borrar(id_producto)

        elif opcion == "5":
            gestor.cerrar()
            break

        else:
            print("Opcion invalida. Intente de nuevo.")

if __name__ == "__main__":
    main()