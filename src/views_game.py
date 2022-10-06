import time
from flask import (render_template, send_from_directory, url_for,
                   request, redirect, flash, g)

from models import Jogo
from app import app

from views_user import is_logged

from helpers import recovery_image, delete_file, FormularioJogo


from db import DatabaseManager

with app.app_context():
    g.db = DatabaseManager()
    g.db.init()
    g.db.connect()

@app.route('/')
def index():
    lista = Jogo.select().order_by(Jogo.get_id)
    return render_template('index.html', title='Jogos', jogos=lista, esta_logado=is_logged())


@app.route('/editar/<int:jogo_id>')
def editar(jogo_id):
    if not is_logged():
        return redirect(url_for('login', proxima=url_for('formulario_novo_jogo')))

    form = FormularioJogo()
    jogo = Jogo.get(Jogo.id == jogo_id)

    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recovery_image(jogo_id)

    return render_template('editar.html', title='Editando jogo', id=jogo.id, capa_jogo=capa_jogo, form=form)


@app.route('/atualizar', methods=['POST'])
def update():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():

        jogo = Jogo.get_by_id(request.form['id'])
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        upload_path = app.config['UPLOAD_PATH']
        arquivo = request.files['arquivo']

        timestamp = time.time()
        delete_file(jogo.id)
        arquivo.save(f'{upload_path}/capa_{jogo.id}_{timestamp}.jpg')

        jogo.save()

    return redirect(url_for('index'))


@app.route('/deletar/<int:jogo_id>')
def delete(jogo_id):
    if not is_logged():
        return redirect(url_for('login'))

    Jogo.get_by_id(jogo_id).delete_instance()
    flash('Jogo deletado com sucesso!')

    return redirect(url_for('index'))


@app.route('/novo')
def formulario_novo_jogo():
    if not is_logged():
        return redirect(url_for('login', proxima=url_for('formulario_novo_jogo')))

    form = FormularioJogo()

    return render_template('novo.html', title='Adicionar um novo jogo', form=form)


@app.route('/create', methods=['POST'])
def create():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    j = Jogo(nome=nome, categoria=categoria, console=console)
    j.save()

    upload_path = app.config['UPLOAD_PATH']
    arquivo = request.files['arquivo']
    arquivo.save(f'{upload_path}/capa_{j.id}.jpg')

    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def image(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


