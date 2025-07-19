from flask import Flask
from controllers.routes import main
import os
from config import UPLOAD_FOLDER

app = Flask(__name__)
app.register_blueprint(main)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
