from flask import (render_template, url_for, request,
                   redirect, session, flash)

from flask_bcrypt import generate_password_hash, check_password_hash

from models import Usuario
from helpers import FormularioLogin, FormularioCadastro

from app import app


@app.route('/login')
def login():
    form = FormularioLogin()

    proxima = request.args.get('proxima', None)
    return render_template('login.html', proxima=proxima, form=form)


@app.route('/logout')
def logout():
    if not is_logged():
        return redirect(url_for('index'))

    usuario = session.pop('usuario_logado', None)
    if usuario:
        flash(f'{usuario} deslogado efetuado com sucesso')

    return redirect(url_for('index'))


@app.route('/cadastro')
def cadastro():
    form = FormularioCadastro()
    return render_template('cadastro.html', form=form)


@app.route('/registrar', methods=['POST'])
def registrar_usuario():

    form = FormularioCadastro(request.form)

    nome = form.nome.data
    nickname = form.nickname.data
    senha = generate_password_hash(form.senha.data)

    if nome is not None and len(nome) >= 3:
        u = Usuario(nome=nome, nickname=nickname, senha=senha)
        u.save()
        flash('Usuário {} cadastrado com sucesso!'.format(nickname))
        return redirect(url_for('login'))

    else:
        flash('Preencha o formulário corretamente')
        return redirect(url_for('cadastro'))


@app.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioLogin(request.form)

    user = Usuario.get(Usuario.nickname == form.nickname.data)
    user_passwd = check_password_hash(user.senha, form.senha.data)

    if user and user_passwd:
        session['usuario_logado'] = user.nickname
        flash('Usuário {} logado com sucesso!'.format(user.nickname))
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)

    flash('Usuario/Senha estão incorretos. Por favor tente novamente.')
    return redirect(url_for('login'))

def is_logged():
    return 'usuario_logado' in session and session['usuario_logado'] is not None
