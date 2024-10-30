import os
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, SelectField, BooleanField, DateField, IntegerField,TextAreaField,EmailField
from wtforms.validators import InputRequired, Regexp, DataRequired, Length
from datetime import date

class FormularioUsuario(FlaskForm):
    login = StringField('Nome de Login', [validators.DataRequired(), validators.Length(min=8, max=20)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=8, max=50)],render_kw={"placeholder": "Insira seu usuário ou e-mail"})
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=4, max=100)],render_kw={"placeholder": "Insira sua senha"})
    entrar = SubmitField('Entrar')