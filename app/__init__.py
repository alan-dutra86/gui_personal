from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')

    from .routes import main
    app.register_blueprint(main)

    return app
