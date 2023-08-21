from conexion import *
from colorama import Fore, Style
from rich import print
from rich.table import Table

def imprimir_encabezado(texto, color):
    print(f"{color}{texto}", Style.RESET_ALL)

def calcular_total(carrito):
    total = sum(producto[3] for producto in carrito)
    return total

def imprimir_tabla_rich(headers, data):
    table = Table(title="Tabla")
    for header in headers:
        table.add_column(header)
    for row in data:
        table.add_row(*row)
    print(table)

def imprimir_producto_rich(producto):
    print(f"  {Fore.YELLOW}ID:{Style.RESET_ALL} {producto[0]}")
    print(f"  {Fore.YELLOW}Nombre:{Style.RESET_ALL} {producto[1]}")
    print(f"  {Fore.YELLOW}Descripción:{Style.RESET_ALL} {producto[2]}")
    print(f"  {Fore.YELLOW}Precio:{Style.RESET_ALL} {producto[3]}")
    print("-" * 40)

def menu_usuario(conexion):
    carrito = []

    while True:
        imprimir_encabezado("\n🛒 Menú de Usuario", Fore.YELLOW)
        print("1. Listar productos")
        print("2. Buscar productos por nombre")
        print("3. Agregar producto al carrito")
        print("4. Ver carrito")
        print("5. Completar compra")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            productos = listar_productos(conexion)
            headers = ["ID", "Nombre", "Descripción", "Precio"]
            data = [[str(producto[0]), producto[1], producto[2], str(producto[3])] for producto in productos]
            imprimir_tabla_rich(headers, data)
        elif opcion == '2':
            nombre_buscar = input("Ingrese el nombre del producto a buscar: ")
            productos_encontrados = buscar_producto_por_nombre(conexion, nombre_buscar)
            headers = ["ID", "Nombre", "Descripción", "Precio"]
            data = [[str(producto[0]), producto[1], producto[2], str(producto[3])] for producto in productos_encontrados]
            imprimir_tabla_rich(headers, data)
        elif opcion == '3':
            id_producto = int(input("Ingrese el ID del producto a agregar al carrito: "))
            producto = buscar_producto_por_id(conexion, id_producto)
            if producto:
                carrito.append(producto)
                print("Producto agregado al carrito.")
            else:
                print("Producto no encontrado.")
        elif opcion == '4':
            if carrito:
                for producto in carrito:
                    imprimir_producto_rich(producto)
                    print("-" * 40)  # Separador entre productos
            else:
                print("El carrito está vacío.")
        elif opcion == '5':
            if carrito:
                total = calcular_total(carrito)
                print(f"Total de compra: {Fore.GREEN}${total}{Style.RESET_ALL}")
                carrito = []
            else:
                print("El carrito está vacío. No se puede completar la compra.")
        elif opcion == '6':
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

def menu_admin(conexion):
    while True:
        imprimir_encabezado("\n🔧 Menú del Administrador", Fore.CYAN)
        print("1. Agregar producto")
        print("2. Editar producto")
        print("3. Eliminar producto")
        print("4. Ver lista de productos")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Nombre del producto: ")
            descripcion = input("Descripción del producto: ")
            precio = float(input("Precio del producto: "))
            insertar_producto(conexion, nombre, descripcion, precio)
            print("Producto agregado con éxito.")
        elif opcion == '2':
            id_producto = int(input("Ingrese el ID del producto a editar: "))
            producto_lista = list(buscar_producto_por_id(conexion, id_producto))
            if producto_lista:
                print(f"Editando producto: {producto_lista[1]}")
                nuevo_nombre = input("Nuevo nombre (Dejar en blanco para mantener): ")
                nueva_descripcion = input("Nueva descripción (Dejar en blanco para mantener): ")
                nuevo_precio = float(input("Nuevo precio (Dejar en blanco para mantener): "))
                if nuevo_nombre:
                    producto_lista[1] = nuevo_nombre
                if nueva_descripcion:
                    producto_lista[2] = nueva_descripcion
                if nuevo_precio:
                    producto_lista[3] = nuevo_precio
                editar_producto(conexion, id_producto, producto_lista[1], producto_lista[2], producto_lista[3])
                print("Producto editado con éxito.")
            else:
                print("Producto no encontrado.")
        elif opcion == '3':
            id_producto = int(input("Ingrese el ID del producto a eliminar: "))
            producto = buscar_producto_por_id(conexion, id_producto)
            if producto:
                eliminar_producto(conexion, id_producto)
                print("Producto eliminado con éxito.")
            else:
                print("Producto no encontrado.")
        elif opcion == '4':
            productos = listar_productos(conexion)
            headers = ["ID", "Nombre", "Descripción", "Precio"]
            data = [[str(producto[0]), producto[1], producto[2], str(producto[3])] for producto in productos]
            imprimir_tabla_rich(headers, data)
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

def main():
    conexion = crear_conexion()
    crear_tabla_productos(conexion)
    crear_tabla_admin(conexion)

    while True:
        imprimir_encabezado("\n🏁 Menú Principal", Fore.GREEN)
        print("1. Iniciar sesión como Usuario")
        print("2. Iniciar sesión como Administrador")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            menu_usuario(conexion)
        elif opcion == '2':
            usuario = input("Usuario: ")
            contrasena = input("Contraseña: ")
            admin = iniciar_sesion_admin(conexion, usuario, contrasena)
            if admin:
                imprimir_encabezado("Inicio de sesión exitoso como administrador.", Fore.GREEN)
                menu_admin(conexion)
            else:
                imprimir_encabezado("Inicio de sesión fallido como administrador.", Fore.RED)
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

    cerrar_conexion(conexion)

if __name__ == "__main__":
    main()
