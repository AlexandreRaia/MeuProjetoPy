from flask import render_template, request, redirect, url_for, jsonify, flash
from models import db, Subunidade, Unidade
import logging
from sqlalchemy.exc import IntegrityError

def listar_subunidades(unidade_id):
    try:
        unidade = Unidade.query.get_or_404(unidade_id)
        subunidades = Subunidade.query.filter_by(unidade_id=unidade_id).all()
        return render_template('subunidade/listar_subunidades.html', unidade=unidade, subunidades=subunidades)
    except Exception as e:
        logging.error(f"Erro ao listar subunidades: {e}", exc_info=True)
        return jsonify(error="Erro ao listar subunidades"), 500

def listar_todas_subunidades():
    try:
        subunidades = Subunidade.query.all()
        logging.debug(f"Subunidades encontradas: {subunidades}")
        return render_template('subunidade/listar_todas_subunidades.html', subunidades=subunidades)
    except Exception as e:
        logging.error(f"Erro ao listar todas as subunidades: {e}", exc_info=True)
        return jsonify(error="Erro ao listar todas as subunidades"), 500

def adicionar_subunidade(unidade_id):
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            sigla = request.form['sigla']
            # Verificar se a sigla já existe
            if Subunidade.query.filter_by(sigla=sigla).first():
                flash('Erro: A sigla informada já está cadastrada.', 'danger')
                return redirect(url_for('subunidade_adicionar', unidade_id=unidade_id))
            nova_subunidade = Subunidade(nome=nome, sigla=sigla, unidade_id=unidade_id)
            db.session.add(nova_subunidade)
            db.session.commit()
            flash('Subunidade adicionada com sucesso!', 'success')
            return redirect(url_for('unidades'))
        except IntegrityError:
            logging.error("Erro: A sigla informada já está cadastrada.", exc_info=True)
            db.session.rollback()
            flash('Erro: A sigla informada já está cadastrada.', 'danger')
            return redirect(url_for('subunidade_adicionar', unidade_id=unidade_id))
        except Exception as e:
            logging.error(f"Erro ao adicionar subunidade: {e}", exc_info=True)
            db.session.rollback()
            flash('Erro ao adicionar subunidade.', 'danger')
            return redirect(url_for('subunidade_adicionar', unidade_id=unidade_id))
    return render_template('subunidade/adicionar_subunidade.html', unidade_id=unidade_id)

def editar_subunidade(id):
    subunidade = Subunidade.query.get_or_404(id)
    if request.method == 'POST':
        try:
            subunidade.nome = request.form['nome']
            subunidade.sigla = request.form['sigla']
            db.session.commit()
            flash('Subunidade editada com sucesso!', 'success')
            return redirect(url_for('subunidades', unidade_id=subunidade.unidade_id))
        except IntegrityError:
            logging.error("Erro: A sigla informada já está cadastrada.", exc_info=True)
            db.session.rollback()
            flash('Erro: A sigla informada já está cadastrada.', 'danger')
            return redirect(url_for('subunidade_editar', id=id))
        except Exception as e:
            logging.error(f"Erro ao editar subunidade: {e}", exc_info=True)
            db.session.rollback()
            flash('Erro ao editar subunidade.', 'danger')
            return redirect(url_for('subunidade_editar', id=id))
    return render_template('subunidade/editar_subunidade.html', subunidade=subunidade)

def excluir_subunidade(id):
    try:
        subunidade = Subunidade.query.get_or_404(id)
        unidade_id = subunidade.unidade_id
        db.session.delete(subunidade)
        db.session.commit()
        flash('Subunidade excluída com sucesso!', 'success')
    except Exception as e:
        logging.error(f"Erro ao excluir subunidade: {e}", exc_info=True)
        db.session.rollback()
        flash(f'Erro ao excluir subunidade: {str(e)}', 'danger')
    return redirect(url_for('subunidades', unidade_id=unidade_id))
