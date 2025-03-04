from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Unidade(db.Model):
    __tablename__ = 'unidade'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sigla = db.Column(db.String(10), nullable=False)
    subunidades = db.relationship('Subunidade', backref='unidade', lazy=True)

class Subunidade(db.Model):
    __tablename__ = 'subunidade'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sigla = db.Column(db.String(10), nullable=False)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidade.id'), nullable=False)
