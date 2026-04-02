import re
from datetime import datetime

def validar_nombre(nombre):
    patron = r'^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$'
    return re.match(patron, nombre) is not None

def validar_precio(precio):
    try:
        precio = float(precio)
        return precio > 0
    except ValueError:
        return False

def validar_total(total):
    try:
        total = float(total)
        return total > 0
    except ValueError:
        return False

def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validar_cantidad(cantidad):
    try:
        cantidad = int(cantidad)
        return cantidad > 0
    except ValueError:
        return False
    
def validar_metodo_pago(metodo_pago):
    metodo_pago = metodo_pago.strip()
    patron = r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$'
    return re.match(patron, metodo_pago) is not None and metodo_pago != ""