from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from models import db, Unidade, Subunidade

def init_app(app: Flask):
    app.secret_key = 'supersecretkey'  # Adicione uma chave secreta para usar flash messages

    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('index.html')
     
    @app.route('/Sobre')
    def Sobre():
        return render_template('sobre.html')
    
    @app.route('/unidades')
    def listar_unidades():
        unidades = Unidade.query.all()
        return render_template('unidade/listar_unidades.html', unidades=unidades)
    
    @app.route('/unidade/adicionar', methods=['GET', 'POST'])
    def adicionar_unidade():
        if request.method == 'POST':
            nome = request.form['nome']
            sigla = request.form['sigla']
            nova_unidade = Unidade(nome=nome, sigla=sigla)
            db.session.add(nova_unidade)
            db.session.commit()
            return redirect(url_for('listar_unidades'))
        return render_template('unidade/adicionar_unidade.html')
    
    @app.route('/unidade/editar/<int:id>', methods=['GET', 'POST'])
    def editar_unidade(id):
        unidade = Unidade.query.get_or_404(id)
        if request.method == 'POST':
            unidade.nome = request.form['nome']
            unidade.sigla = request.form['sigla']
            db.session.commit()
            return redirect(url_for('listar_unidades'))
        return render_template('unidade/editar_unidade.html', unidade=unidade)
    
    @app.route('/unidade/excluir/<int:id>', methods=['POST'])
    def excluir_unidade(id):
        try:
            unidade = Unidade.query.get_or_404(id)
            db.session.delete(unidade)
            db.session.commit()
            flash('Unidade excluída com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao excluir unidade: {str(e)}', 'danger')
        return redirect(url_for('listar_unidades'))
    
    @app.route('/subunidades/<int:unidade_id>')
    def listar_subunidades(unidade_id):
        unidade = Unidade.query.get_or_404(unidade_id)
        return render_template('subunidade/listar_subunidades.html', unidade=unidade)
    
    @app.route('/subunidades')
    def listar_todas_subunidades():
        subunidades = Subunidade.query.all()
        return render_template('subunidade/listar_todas_subunidades.html', subunidades=subunidades)
    
    @app.route('/subunidade/adicionar/<int:unidade_id>', methods=['GET', 'POST'])
    def adicionar_subunidade(unidade_id):
        if request.method == 'POST':
            nome = request.form['nome']
            sigla = request.form['sigla']
            nova_subunidade = Subunidade(nome=nome, sigla=sigla, unidade_id=unidade_id)
            db.session.add(nova_subunidade)
            db.session.commit()
            return redirect(url_for('listar_subunidades', unidade_id=unidade_id))
        return render_template('subunidade/adicionar_subunidade.html', unidade_id=unidade_id)
    
    @app.route('/subunidade/editar/<int:id>', methods=['GET', 'POST'])
    def editar_subunidade(id):
        subunidade = Subunidade.query.get_or_404(id)
        if request.method == 'POST':
            subunidade.nome = request.form['nome']
            subunidade.sigla = request.form['sigla']
            db.session.commit()
            return redirect(url_for('listar_subunidades', unidade_id=subunidade.unidade_id))
        return render_template('subunidade/editar_subunidade.html', subunidade=subunidade)
    
    @app.route('/subunidade/excluir/<int:id>', methods=['POST'])
    def excluir_subunidade(id):
        try:
            subunidade = Subunidade.query.get_or_404(id)
            unidade_id = subunidade.unidade_id
            db.session.delete(subunidade)
            db.session.commit()
            flash('Subunidade excluída com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao excluir subunidade: {str(e)}', 'danger')
        return redirect(url_for('listar_subunidades', unidade_id=unidade_id))
    
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(error="Página não encontrada"), 404
