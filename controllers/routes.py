from flask import Blueprint, request, render_template, send_file
from pathlib import Path
from config import KEY_FILE_AES, KEY_FILE_HMAC, UPLOAD_FOLDER
from services.encriptado import generar_claves, encriptar, desencriptar
from services.archivo import guardar_archivo, leer_archivo, archivo_existe

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/encrypt', methods=['POST'])
def encrypt():
    file = request.files.get('file')
    if not file or not file.filename.endswith('.xlsx'):
        return "❌ Archivo no válido", 400

    original = Path(file.filename).stem
    encrypted_filename = f"{original}.enc"
    encrypted_path = Path(UPLOAD_FOLDER) / encrypted_filename

    # Genera ambas claves y encripta
    clave_aes, clave_hmac = generar_claves()
    contenido = file.read()
    cifrado = encriptar(contenido, clave_aes, clave_hmac)

    # Guarda archivo cifrado y ambas claves
    guardar_archivo(encrypted_path, cifrado)
    guardar_archivo(KEY_FILE_AES, clave_aes)
    guardar_archivo(KEY_FILE_HMAC, clave_hmac)

    return send_file(
        encrypted_path,
        as_attachment=True,
        download_name=encrypted_filename
    )

@main.route('/decrypt', methods=['POST'])
def decrypt():
    file_enc = request.files.get('file_enc')
    if not file_enc:
        return "❌ Falta el archivo encriptado", 400

    # Verifica que existan ambas claves
    if not (archivo_existe(KEY_FILE_AES) and archivo_existe(KEY_FILE_HMAC)):
        return "❌ No se encontraron las claves", 404

    original = Path(file_enc.filename).stem
    decrypted_filename = f"{original}.xlsx"
    decrypted_path = Path(UPLOAD_FOLDER) / decrypted_filename

    # Carga claves y contenido cifrado
    clave_aes  = leer_archivo(KEY_FILE_AES)
    clave_hmac = leer_archivo(KEY_FILE_HMAC)
    cifrado    = file_enc.read()

    try:
        descifrado = desencriptar(cifrado, clave_aes, clave_hmac)
    except Exception:
        return "❌ Error al desencriptar. Clave incorrecta o archivo dañado.", 400

    guardar_archivo(decrypted_path, descifrado)
    return send_file(
        decrypted_path,
        as_attachment=True,
        download_name=decrypted_filename
    )
