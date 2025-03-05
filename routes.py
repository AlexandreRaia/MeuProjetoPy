from flask import Flask, render_template, jsonify
from controllers.unidade_controller import listar_unidades, adicionar_unidade, editar_unidade, excluir_unidade
from controllers.subunidade_controller import listar_subunidades, listar_todas_subunidades, adicionar_subunidade, editar_subunidade, excluir_subunidade
from controllers.veiculo_controller import listar_veiculos, adicionar_veiculo, editar_veiculo, excluir_veiculo
from models import Unidade, Subunidade, Veiculo
import logging

def init_app(app: Flask):
    app.secret_key = 'supersecretkey'  # Adicione uma chave secreta para usar flash messages

    @app.route('/')
    @app.route('/home')
    def home():
        unidades_count = Unidade.query.count()
        subunidades_count = Subunidade.query.count()
        veiculos_count = Veiculo.query.count()
        return render_template('index.html', unidades_count=unidades_count, subunidades_count=subunidades_count, veiculos_count=veiculos_count)
     
    @app.route('/Sobre')
    def Sobre():
        return render_template('sobre.html')
    
    @app.route('/unidades')
    def unidades():
        return listar_unidades()
    
    @app.route('/unidade/adicionar', methods=['GET', 'POST'])
    def unidade_adicionar():
        return adicionar_unidade()
    
    @app.route('/unidade/editar/<int:id>', methods=['GET', 'POST'])
    def unidade_editar(id):
        return editar_unidade(id)
    
    @app.route('/unidade/excluir/<int:id>', methods=['POST'])
    def unidade_excluir(id):
        return excluir_unidade(id)
    
    @app.route('/subunidades/<int:unidade_id>')
    def subunidades(unidade_id):
        return listar_subunidades(unidade_id)
    
    @app.route('/subunidades')
    def todas_subunidades():
        return listar_todas_subunidades()
    
    @app.route('/subunidade/adicionar/<int:unidade_id>', methods=['GET', 'POST'])
    def subunidade_adicionar(unidade_id):
        return adicionar_subunidade(unidade_id)
    
    @app.route('/subunidade/editar/<int:id>', methods=['GET', 'POST'])
    def subunidade_editar(id):
        return editar_subunidade(id)
    
    @app.route('/subunidade/excluir/<int:id>', methods=['POST'])
    def subunidade_excluir(id):
        return excluir_subunidade(id)
    
    @app.route('/veiculos')
    def veiculos():
        return listar_veiculos()
    
    @app.route('/veiculo/adicionar', methods=['GET', 'POST'])
    def veiculo_adicionar():
        return adicionar_veiculo()
    
    @app.route('/veiculo/editar/<int:id>', methods=['GET', 'POST'])
    def veiculo_editar(id):
        return editar_veiculo(id)
    
    @app.route('/veiculo/excluir/<int:id>', methods=['POST'])
    def veiculo_excluir(id):
        return excluir_veiculo(id)
    
    @app.errorhandler(404)
    def page_not_found(e):
        logging.error(f"Página não encontrada: {e}")
        return jsonify(error="Página não encontrada"), 404
