import os
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class FormularioJogo(FlaskForm):
    nome = StringField(label='Nome do jogo', validators=[validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField(label='Categoria', validators=[validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField(label='Console', validators=[validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField(label='Salvar')


class FormularioUsuario(FlaskForm):
    nickname = StringField(label='Nickname', validators=[validators.DataRequired(), validators.Length(min=1, max=13)])
    nome = StringField(label='Nome Completo', validators=[validators.DataRequired(), validators.Length(min=1, max=50)])
    senha = PasswordField(label='Senha', validators=[validators.DataRequired(), validators.Length(min=1, max=13)])


class FormularioCadastro(FormularioUsuario):
    criar = SubmitField(label='Cadastrar')


class FormularioLogin(FormularioUsuario):
    login = SubmitField(label='Login')



def recovery_image(game_id):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{game_id}.jpg' in file_name:
            return file_name

    return 'capa_padrap.jpg'


def delete_file(game_id):
    file = recovery_image(game_id)
    if file != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))
