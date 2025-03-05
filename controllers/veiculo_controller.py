from flask import render_template, request, redirect, url_for, jsonify, flash
from models import db, Veiculo
import logging
from sqlalchemy.exc import IntegrityError

def listar_veiculos():
    try:
        veiculos = Veiculo.query.all()
        return render_template('veiculo/listar_veiculos.html', veiculos=veiculos)
    except Exception as e:
        logging.error(f"Erro ao listar veículos: {e}", exc_info=True)
        return jsonify(error="Erro ao listar veículos"), 500

def adicionar_veiculo():
    if request.method == 'POST':
        try:
            marca = request.form['marca']
            modelo = request.form['modelo']
            tipo = request.form['tipo']
            placa = request.form['placa']
            novo_veiculo = Veiculo(marca=marca, modelo=modelo, tipo=tipo, placa=placa)
            db.session.add(novo_veiculo)
            db.session.commit()
            flash('Veículo adicionado com sucesso!', 'success')
            return redirect(url_for('veiculos'))
        except IntegrityError:
            logging.error("Erro: A placa informada já está cadastrada.", exc_info=True)
            db.session.rollback()
            flash('Erro: A placa informada já está cadastrada.', 'danger')
            return redirect(url_for('veiculos'))
        except Exception as e:
            logging.error(f"Erro ao adicionar veículo: {e}", exc_info=True)
            db.session.rollback()
            return jsonify(error="Erro ao adicionar veículo"), 500
    return render_template('veiculo/adicionar_veiculo.html')

def editar_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    if request.method == 'POST':
        try:
            veiculo.marca = request.form['marca']
            veiculo.modelo = request.form['modelo']
            veiculo.tipo = request.form['tipo']
            veiculo.placa = request.form['placa']
            db.session.commit()
            flash('Veículo editado com sucesso!', 'success')
            return redirect(url_for('veiculos'))
        except IntegrityError:
            logging.error("Erro: A placa informada já está cadastrada.", exc_info=True)
            db.session.rollback()
            flash('Erro: A placa informada já está cadastrada.', 'danger')
            return redirect(url_for('veiculos'))
        except Exception as e:
            logging.error(f"Erro ao editar veículo: {e}", exc_info=True)
            db.session.rollback()
            return jsonify(error="Erro ao editar veículo"), 500
    return render_template('veiculo/editar_veiculo.html', veiculo=veiculo)

def excluir_veiculo(id):
    try:
        veiculo = Veiculo.query.get_or_404(id)
        db.session.delete(veiculo)
        db.session.commit()
        flash('Veículo excluído com sucesso!', 'success')
    except Exception as e:
        logging.error(f"Erro ao excluir veículo: {e}", exc_info=True)
        db.session.rollback()
        flash(f'Erro ao excluir veículo: {str(e)}', 'danger')
    return redirect(url_for('veiculos'))
