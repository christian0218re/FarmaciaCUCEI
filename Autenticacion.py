# Autenticacion.py
from BaseDatos import conectar

def iniciar_sesion(correo, contraseña):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT usuarioId, rol FROM usuarios WHERE correo = ? AND contraseña = ?", (correo, contraseña))
    usuario = cursor.fetchone()
    conn.close()
    if usuario:
        return usuario  # Retorna el usuarioId y el rol
    else:
        return None  # Usuario no encontrado o contraseña incorrecta

def tiene_permiso(rol, accion):
    permisos = {
        'Admin': ['All'],
        'Gerente': ['CRUD Clientes', 'CRUD Ventas'],
        'Cajero': ['CR Clientes', 'CR Ventas'],
    }
    return accion in permisos[rol]
