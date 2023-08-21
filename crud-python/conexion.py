import sqlite3

def crear_conexion():
    conexion = sqlite3.connect('database.db')
    return conexion

def cerrar_conexion(conexion):
    conexion.close()

def crear_tabla_productos(conexion):
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
        ID INTEGER PRIMARY KEY,
        NOMBRE TEXT,
        DESCRIPCION TEXT,
        PRECIO REAL
    )''')
    conexion.commit()

def crear_tabla_admin(conexion):
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
        ID INTEGER PRIMARY KEY,
        USUARIO TEXT,
        CONTRASENA TEXT
    )''')
    conexion.commit()

def insertar_producto(conexion, nombre, descripcion, precio):
    cursor = conexion.cursor()
    cursor.execute('''INSERT INTO productos (NOMBRE, DESCRIPCION, PRECIO) VALUES (?, ?, ?)''',
                   (nombre, descripcion, precio))
    conexion.commit()

def buscar_producto_por_id(conexion, id_producto):
    cursor = conexion.cursor()
    cursor.execute('''SELECT * FROM productos WHERE ID = ?''', (id_producto,))
    producto = cursor.fetchone()
    return producto

def buscar_producto_por_nombre(conexion, nombre):
    cursor = conexion.cursor()
    cursor.execute('''SELECT * FROM productos WHERE NOMBRE LIKE ?''', ('%' + nombre + '%',))
    productos = cursor.fetchall()
    return productos

def editar_producto(conexion, id_producto, nombre, descripcion, precio):
    cursor = conexion.cursor()
    cursor.execute('''UPDATE productos SET NOMBRE = ?, DESCRIPCION = ?, PRECIO = ? WHERE ID = ?''',
                   (nombre, descripcion, precio, id_producto))
    conexion.commit()

def eliminar_producto(conexion, id_producto):
    cursor = conexion.cursor()
    cursor.execute('''DELETE FROM productos WHERE ID = ?''', (id_producto,))
    conexion.commit()

def listar_productos(conexion):
    cursor = conexion.cursor()
    cursor.execute('''SELECT * FROM productos''')
    productos = cursor.fetchall()
    return productos

def iniciar_sesion_admin(conexion, usuario, contrasena):
    cursor = conexion.cursor()
    cursor.execute('''SELECT * FROM admin WHERE USUARIO = ? AND CONTRASEÑA = ?''', (usuario, contrasena))
    admin = cursor.fetchone()
    return admin
