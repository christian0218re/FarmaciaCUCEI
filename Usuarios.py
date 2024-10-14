# Usuarios.py
from baseDatos import conectar

def crear_usuario(nombre, correo, contraseña, rol, direccion=None, telefono=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nombre, correo, contraseña, rol, direccion, telefono)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, correo, contraseña, rol, direccion, telefono))
    conn.commit()
    conn.close()

def leer_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def actualizar_usuario(usuarioId, nombre, correo, contraseña, rol, direccion=None, telefono=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET nombre = ?, correo = ?, contraseña = ?, rol = ?, direccion = ?, telefono = ?
        WHERE usuarioId = ?
    """, (nombre, correo, contraseña, rol, direccion, telefono, usuarioId))
    conn.commit()
    conn.close()

def eliminar_usuario(usuarioId):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE usuarioId = ?", (usuarioId,))
    conn.commit()
    conn.close()
