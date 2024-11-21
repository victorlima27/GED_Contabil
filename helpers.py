from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, SelectField, BooleanField, DateField, IntegerField,TextAreaField,EmailField, MultipleFileField,FileField
from wtforms.validators import InputRequired, Regexp, DataRequired, Length
from flask_wtf.file import FileAllowed

class FormularioUsuario(FlaskForm):
    login = StringField('Nome de Login', [validators.DataRequired(), validators.Length(min=8, max=20)])
    cpf = StringField('CPF', validators=[DataRequired(),Length(max=14)], render_kw={'oninput': 'formatarCPF(this)',"placeholder": "Insira seu CPF (somente números)"})
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=4, max=100)],render_kw={"placeholder": "Insira sua senha"})
    entrar = SubmitField('Entrar')
class FormularioCriarUsuario(FlaskForm):
    nome_usu = StringField('Nome do Usuário:', [validators.DataRequired(), validators.Length(min=1, max=20)],render_kw={"placeholder": "Informe o nome do usuário (Ex.: Nome Sobrenome)"})
    login = StringField('Login:', [validators.DataRequired(), validators.Length(min=1, max=20)],render_kw={"placeholder": "Informe o login do usuário (Ex.: nome.sobrenome)"})
    email = StringField('Email:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "Insira o e-mail para que realize o acesso"})
    perfil = SelectField('Perfil:')
    departamento = SelectField('Departamento:')
    senha = PasswordField('Caso deseje alterar a senha:', [validators.Length(min=1, max=100)],render_kw={"placeholder": "Insira a senha"})
    ativo = BooleanField('Usuário Ativo', default=True)
    criar = SubmitField('Criar')
    deletar = SubmitField('Criar')
class FormularioPesquisarUsuario(FlaskForm):
    nome_usu = StringField('Nome do Usuário:', [validators.DataRequired(), validators.Length(min=1, max=20)],render_kw={"placeholder": "Informe o nome do usuário (Ex.: Nome Sobrenome)"})
    login = StringField('Login:', [validators.DataRequired(), validators.Length(min=1, max=20)],render_kw={"placeholder": "Informe o login do usuário (Ex.: nome.sobrenome)"})
    email = StringField('Email:', [validators.DataRequired(), validators.Length(min=1, max=50)],render_kw={"placeholder": "Insira o e-mail para que realize o acesso"})
    perfil = SelectField('Perfil:')
    departamento = SelectField('Departamento:')
    senha = PasswordField('Caso deseje alterar a senha:', [validators.Length(min=1, max=100)],render_kw={"placeholder": "Insira a senha"})
    ativo = BooleanField('Usuário Ativo', default=True)
    criar = SubmitField('Salvar')
    deletar = SubmitField('Criar')
class FormularioMeuPerfil(FlaskForm):
    nome_usu = StringField('Nome do Usuário:', [validators.DataRequired(), validators.Length(min=1, max=20)],render_kw={"placeholder": "Informe o nome do usuário (Ex.: Nome Sobrenome)"})
    login = StringField('Login:', [validators.DataRequired(), validators.Length(min=8, max=20)],render_kw={"placeholder": "Informe o login do usuário (Ex.: nome.sobrenome)"})
    email = StringField('Email:', [validators.DataRequired(), validators.Length(min=8, max=50)],render_kw={"placeholder": "Insira o e-mail para que realize o acesso"})
    senha_atual = PasswordField('Caso deseje alterar insira sua senha atual:', [validators.Length(min=8, max=100)],render_kw={"placeholder": "Insira a senha atual"})
    senha = PasswordField('Caso deseje alterar a nova senha:', [validators.Length(min=8, max=100)],render_kw={"placeholder": "Insira a nova senha"})
    criar = SubmitField('Salvar')

class UploadForm(FlaskForm):
    files = MultipleFileField('NFS/NFSe', validators=[validators.DataRequired(),FileAllowed(['pdf', 'xml'], 'Apenas arquivos PDF e XML são permitidos!')])
    submit = SubmitField('Enviar')

class UploadFormExtrato(FlaskForm):
    files_pdf= FileField('PDF/A', validators=[validators.DataRequired(),FileAllowed(['.pdf'], 'Apenas arquivos PDF são permitidos!')])
    files_ofx = FileField('OFX', validators=[validators.DataRequired(),FileAllowed(['.ofx'], 'Apenas arquivos OFX são permitidos!')])
    banco = SelectField('Banco', validators=[validators.DataRequired()],render_kw={"placeholder": "Informe o banco"})
    submit = SubmitField('Enviar')