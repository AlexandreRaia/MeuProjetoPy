from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Unidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sigla = db.Column(db.String(10), nullable=False, unique=True)
    subunidades = db.relationship('Subunidade', backref='unidade', lazy=True)

class Subunidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sigla = db.Column(db.String(10), nullable=False, unique=True)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidade.id'), nullable=False)

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    placa = db.Column(db.String(10), nullable=False, unique=True)