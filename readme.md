# Proyecto Encriptador IPS

## Descripción

Este proyecto proporciona una aplicación web construida con Flask para **encriptar y desencriptar** archivos Excel (`.xlsx`) usando **AES-256 en modo CBC** combinado con **HMAC-SHA256**. La técnica **Encrypt-then-MAC** garantiza tanto la confidencialidad como la integridad de los datos. Los archivos cifrados tienen la extensión `.enc`.

---

## Requisitos

- **Python 3.8+**
- **pip** (gestor de paquetes de Python)
- Paquete **pycryptodome** para AES y HMAC
- Acceso a Internet para CDN de Bootstrap

---

## Estructura del Proyecto

```
ProyectoEncriptadorIPS/               # repositorio
│
├── config.py                         # Configuración: BLOCK_SIZE, KEY_SIZE, HMAC_KEY_SIZE, KEY_FILE_AES, KEY_FILE_HMAC, UPLOAD_FOLDER
├── encriptado.py                     # Arranque de la aplicación Flask
├── controllers/
│   └── routes.py                     # Definición de rutas y lógica de Flask (encrypt & decrypt adaptados a dos claves)
├── services/
│   ├── archivo.py                    # Utilidades para I/O de archivos
│   └── encriptado/
│       ├── aes_cbc.py                # Funciones AES-CBC: generar clave, cifrar, descifrar
│       └── aes_hmac.py               # Funciones Encrypt-then-MAC (HMAC-SHA256)
├── templates/
│   └── index.html                    # Vista HTML con Bootstrap
└── uploads/                          # Archivos temporales y claves (clave_aes.key, clave_hmac.key)
```

---

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/lfernandoass/Encriptador-Base-IPS.git
   cd Encriptador-Base-IPS
   ```

2. Crea un entorno virtual (opcional pero recomendado):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Unix/macOS
   venv\Scripts\activate     # Windows
   ```

3. Instala las dependencias:

   ```bash
   pip install flask pycryptodome
   ```

---

## Uso

1. **Ejecutar la aplicación**:

   ```bash
   python encriptado.py
   ```

   La aplicación estará disponible en `http://127.0.0.1:5000`.

2. **Encriptar un archivo**:

   - En *Encriptar archivo Excel*, selecciona un `.xlsx`.
   - Haz clic en **Encriptar y descargar .enc**.
   - Se descargará un archivo con extensión `.enc` que incluye IV || ciphertext || HMAC.

3. **Desencriptar un archivo**:

   - En *Desencriptar archivo .enc*, selecciona el `.enc` generado.
   - Haz clic en **Desencriptar y descargar .xlsx**.
   - Se valida HMAC antes de descifrar y luego se descarga el Excel original.

---

## Notas de Seguridad

- Se generan **dos claves** aleatorias:
  - `clave_aes.key` (32 bytes) para AES-256
  - `clave_hmac.key` (32 bytes) para HMAC-SHA256
- Las claves se guardan en `uploads/`.
- El orden **Encrypt-then-MAC** verifica la integridad antes de descifrar, previniendo ataques de padding oracle.
- En producción, protege `uploads/`, rota claves periódicamente y **desactiva** `debug=True`.

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta `LICENSE` para más detalles.

---

