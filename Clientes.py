# Clientes.py
from baseDatos import conectar

def crear_cliente(nombre, correo=None, direccion=None, telefono=None, puntos=0):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nombre, correo, direccion, telefono, puntos)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, correo, direccion, telefono, puntos))
    conn.commit()
    conn.close()

def leer_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def actualizar_cliente(clienteId, nombre, correo=None, direccion=None, telefono=None, puntos=0):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes
        SET nombre = ?, correo = ?, direccion = ?, telefono = ?, puntos = ?
        WHERE clienteId = ?
    """, (nombre, correo, direccion, telefono, puntos, clienteId))
    conn.commit()
    conn.close()

def eliminar_cliente(clienteId):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE clienteId = ?", (clienteId,))
    conn.commit()
    conn.close()
