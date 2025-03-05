from flask import render_template, request, redirect, url_for, jsonify, flash
from models import db, Unidade
import logging

def listar_unidades():
    try:
        unidades = Unidade.query.all()
        return render_template('unidade/listar_unidades.html', unidades=unidades)
    except Exception as e:
        logging.error(f"Erro ao listar unidades: {e}", exc_info=True)
        return jsonify(error="Erro ao listar unidades"), 500

def adicionar_unidade():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            sigla = request.form['sigla']
            nova_unidade = Unidade(nome=nome, sigla=sigla)
            db.session.add(nova_unidade)
            db.session.commit()
            flash('Unidade adicionada com sucesso!', 'success')
            return redirect(url_for('unidades'))
        except Exception as e:
            logging.error(f"Erro ao adicionar unidade: {e}", exc_info=True)
            db.session.rollback()
            flash('Erro ao adicionar unidade.', 'danger')
            return redirect(url_for('unidade_adicionar'))
    return render_template('unidade/adicionar_unidade.html')

def editar_unidade(id):
    unidade = Unidade.query.get_or_404(id)
    if request.method == 'POST':
        try:
            unidade.nome = request.form['nome']
            unidade.sigla = request.form['sigla']
            db.session.commit()
            flash('Unidade editada com sucesso!', 'success')
            return redirect(url_for('unidades'))
        except Exception as e:
            logging.error(f"Erro ao editar unidade: {e}", exc_info=True)
            db.session.rollback()
            flash('Erro ao editar unidade.', 'danger')
            return redirect(url_for('unidade_editar', id=id))
    return render_template('unidade/editar_unidade.html', unidade=unidade)

def excluir_unidade(id):
    try:
        unidade = Unidade.query.get_or_404(id)
        db.session.delete(unidade)
        db.session.commit()
        flash('Unidade excluída com sucesso!', 'success')
    except Exception as e:
        logging.error(f"Erro ao excluir unidade: {e}", exc_info=True)
        db.session.rollback()
        flash(f'Erro ao excluir unidade: {str(e)}', 'danger')
    return redirect(url_for('unidades'))
