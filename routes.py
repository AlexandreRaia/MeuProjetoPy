from flask import Flask
from app import app

def init_app(app: Flask):
    @app.route('/')
    def hello_world():
        return 'Olá, mundo!'
