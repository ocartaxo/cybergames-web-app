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
        flash(f'{usuario} deslogado com sucesso')

    return redirect(url_for('index'))


@app.route('/cadastro')
def cadastro():
    form = FormularioCadastro()
    return render_template('cadastro.html', form=form)


@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    form = FormularioCadastro(request.form)

    nome = str(form.nome.data).title()
    nickname = str(form.nickname.data)
    senha = generate_password_hash(form.senha.data).decode('utf-8')

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

    # valores padrão
    msg = 'Usuario e/ou senhas incorretos. Tente novamente!'
    prox_pag = url_for('login')

    form = FormularioLogin(request.form)
    user, user_passwd = get_user(form)

    if user and user_passwd:
        session['usuario_logado'] = user.nickname
        msg = 'Usuário {} logado com sucesso!'.format(user.nickname)
        prox_pag = request.form['proxima']

    flash(msg)
    return redirect(prox_pag)


def get_user(form: FormularioLogin):
    u = Usuario.get_or_none(Usuario.nickname == form.nickname.data)
    u_passwd = check_password_hash(u.senha, form.senha.data) if u is not None else None

    return u, u_passwd


def is_logged():
    return 'usuario_logado' in session and session['usuario_logado'] is not None
