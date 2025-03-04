from flask import Flask
from . import routes
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as rotas
    routes.init_app(app)

    return app