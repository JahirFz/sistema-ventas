import os
import sqlite3
from datetime import datetime


RUTA_DB = os.path.join("database", "ventas.db")
CARPETA_BACKUPS = "backups"


def crear_carpeta_backups():
    if not os.path.exists(CARPETA_BACKUPS):
        os.makedirs(CARPETA_BACKUPS)


def generar_nombre_backup():
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"backup_{fecha}.db"


def crear_backup():
    try:
        crear_carpeta_backups()

        nombre_backup = generar_nombre_backup()
        ruta_backup = os.path.join(CARPETA_BACKUPS, nombre_backup)

        origen = sqlite3.connect(RUTA_DB)
        destino = sqlite3.connect(ruta_backup)

        with destino:
            origen.backup(destino)

        origen.close()
        destino.close()

        return True, ruta_backup

    except Exception as e:
        return False, str(e)
    
    limpiar_backups()

def restaurar_backup(ruta_backup):
    try:
        if not os.path.exists(ruta_backup):
            return False, "El archivo no existe."

        # cerrar conexiones antes (importante)
        if os.path.exists(RUTA_DB):
            os.remove(RUTA_DB)

        origen = sqlite3.connect(ruta_backup)
        destino = sqlite3.connect(RUTA_DB)

        with destino:
            origen.backup(destino)

        origen.close()
        destino.close()

        return True, "Base de datos restaurada correctamente."

    except Exception as e:
        return False, str(e)

def limpiar_backups(max_archivos=10):
    archivos = sorted(
        [f for f in os.listdir(CARPETA_BACKUPS) if f.endswith(".db")],
        reverse=True
    )

    for archivo in archivos[max_archivos:]:
        os.remove(os.path.join(CARPETA_BACKUPS, archivo))