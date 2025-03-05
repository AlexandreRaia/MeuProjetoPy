from flask import Flask
from models import db
from routes import init_app
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meuprojeto.db'
db.init_app(app)

with app.app_context():
    db.create_all()

init_app(app)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)