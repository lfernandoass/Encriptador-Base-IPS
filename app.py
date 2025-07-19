from flask import Flask
from controllers.routes import main
import os
from config import UPLOAD_FOLDER

app = Flask(__name__)
app.register_blueprint(main)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
