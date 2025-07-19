# services/encriptado.py

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA256
from config import BLOCK_SIZE, KEY_SIZE, HMAC_KEY_SIZE

def generar_claves() -> tuple[bytes, bytes]:
    """Devuelve (clave_aes, clave_hmac)."""
    clave_aes  = get_random_bytes(KEY_SIZE)
    clave_hmac = get_random_bytes(HMAC_KEY_SIZE)
    return clave_aes, clave_hmac

def encriptar(data: bytes, clave_aes: bytes, clave_hmac: bytes) -> bytes:
    cipher     = AES.new(clave_aes, AES.MODE_CBC)
    iv         = cipher.iv
    ciphertext = cipher.encrypt(pad(data, BLOCK_SIZE))
    mensaje    = iv + ciphertext

    hmac = HMAC.new(clave_hmac, mensaje, digestmod=SHA256).digest()
    return mensaje + hmac

def desencriptar(data: bytes, clave_aes: bytes, clave_hmac: bytes) -> bytes:
    mac_extraido = data[-32:]
    mensaje      = data[:-32]

    HMAC.new(clave_hmac, mensaje, digestmod=SHA256).verify(mac_extraido)

    iv         = mensaje[:BLOCK_SIZE]
    ciphertext = mensaje[BLOCK_SIZE:]
    cipher     = AES.new(clave_aes, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
