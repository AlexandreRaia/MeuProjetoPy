from flask import Flask
from routes import init_app
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_app(app)

if __name__ == '__main__':
    app.run(debug=True)