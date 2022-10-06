from peewee import (
    Model, CharField, MySQLDatabase
)

database = MySQLDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database


class Jogo(BaseModel):
    nome = CharField(max_length=50)
    categoria = CharField(max_length=40)
    console = CharField(max_length=20)


class Usuario(BaseModel):
    nickname = CharField(max_length=13, unique=True, index=True)
    nome = CharField(max_length=50)
    senha = CharField(max_length=100)
