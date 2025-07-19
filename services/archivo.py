import os

def guardar_archivo(path, contenido: bytes):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(contenido)

def leer_archivo(path) -> bytes:
    with open(path, 'rb') as f:
        return f.read()

def archivo_existe(path) -> bool:
    return os.path.exists(path)
