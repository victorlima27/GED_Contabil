from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import relationship, aliased
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app,db

migrate = Migrate(app,db)

class TipoNF(db.Model):
    __tablename__ = 'tipo_nf'
    id_tipo_nf = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    descricao_nf = db.Column(db.String(100), nullable=True)  # Descrição de até 100 caracteres
    modelo_nf = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<TipoNF %r>' % self.descricao_nf

class TipoErro(db.Model):
    __tablename__ = 'tipo_erro'
    id_erro = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    descricao_erro = db.Column(db.String(255), nullable=True)  # Descrição de erro, geralmente até 255 caracteres

    def __repr__(self):
        return '<TipoErro %r>' % self.descricao_erro

class TipoArquivo(db.Model):
    __tablename__ = 'tipo_arquivo'
    id_tipo_arquivo = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    descricao_arquivo = db.Column(db.String(100), nullable=True)  # Tipo de arquivo, até 100 caracteres

    def __repr__(self):
        return '<TipoArquivo %r>' % self.descricao_arquivo

class Banco(db.Model):
    __tablename__ = 'banco'
    cod_banco = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome_banco = db.Column(db.String(100), nullable=True)  # Nome do banco, 100 caracteres

    def __repr__(self):
        return '<Banco %r>' % self.nome_banco

class Cliente(db.Model):
    __tablename__ = 'cliente'
    cpf_cnpj = db.Column(db.String(14), primary_key=True, nullable=False)  # CPF/CNPJ com até 14 caracteres
    nome_cliente = db.Column(db.String(100), nullable=True)
    telefone_cliente = db.Column(db.String(15), nullable=True)  # Formato de telefone de até 15 caracteres
    endereco_cliente = db.Column(db.Text, nullable=True)
    email_cliente = db.Column(db.String(255), nullable=True)  # E-mail de até 255 caracteres
    senha_cliente = db.Column(db.String(128), nullable=True)  # Senha de até 128 caracteres
    ultimo_login_cliente = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return '<Cliente %r>' % self.nome_cliente

class Arquivo(db.Model):
    __tablename__ = 'arquivo'
    id_arquivo = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id_tipo_arquivo = db.Column(db.Integer, db.ForeignKey('tipo_arquivo.id_tipo_arquivo'), nullable=False)
    cpf_cnpj = db.Column(db.String(14), db.ForeignKey('cliente.cpf_cnpj'), nullable=False)
    nome_arquivo = db.Column(db.String(255), nullable=True)  # Nome de arquivo até 255 caracteres
    data_hora_upload_arquivo = db.Column(db.DateTime, nullable=True)
    tipo_arquivo = db.Column(db.String(50), nullable=True)  # Tipo de arquivo de até 50 caracteres
    url_minio_arquivo = db.Column(db.Text, nullable=True)  # URLs geralmente são textos

    def __repr__(self):
        return '<Arquivo %r>' % self.nome_arquivo

class NotaFiscal(db.Model):
    __tablename__ = 'nota_fiscal'
    id_tipo_nf = db.Column(db.Integer, db.ForeignKey('tipo_nf.id_tipo_nf'), nullable=False)
    id_arquivo = db.Column(db.Integer, db.ForeignKey('arquivo.id_arquivo'), primary_key=True, nullable=False)
    num_nota = db.Column(db.Integer, nullable=True)
    data_emissao_nota = db.Column(db.Date, nullable=True)
    valor_nota = db.Column(db.Float, nullable=True)
    cnpj_emitente_nota = db.Column(db.String(14), nullable=True)  # CNPJ com até 14 caracteres
    cnpj_destinatario_nota = db.Column(db.String(14), nullable=True)
    nota_verificada = db.Column(db.Boolean, nullable=True)
    data_verificacao_nota = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return '<NotaFiscal %r>' % self.num_nota

class ExtratoPdf(db.Model):
    __tablename__ = 'extrato_pdf'
    cod_banco = db.Column(db.Integer, db.ForeignKey('banco.cod_banco'), nullable=False)
    id_arquivo = db.Column(db.Integer, db.ForeignKey('arquivo.id_arquivo'), primary_key=True, nullable=False)
    num_agencia_extrato = db.Column(db.Integer, nullable=True)
    num_conta_extrato = db.Column(db.Integer, nullable=True)
    data_inicial_extrato = db.Column(db.Date, nullable=True)
    data_final_extrato = db.Column(db.Date, nullable=True)
    saldo_inicial_extrato = db.Column(db.Float, nullable=True)
    saldo_final_extrato = db.Column(db.Float, nullable=True)
    id_arquivo_par = db.Column(db.Integer, nullable=True)
    data_verificacao_extrato = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return '<ExtratoPdf %r>' % self.id_arquivo

class Validacao(db.Model):
    __tablename__ = 'validacao'
    id_arquivo = db.Column(db.Integer, db.ForeignKey('arquivo.id_arquivo'), primary_key=True, nullable=False)
    id_erro = db.Column(db.Integer, db.ForeignKey('tipo_erro.id_erro'), nullable=False)
    status_validacao = db.Column(db.Boolean, nullable=True)
    data_hora_validacao = db.Column(db.DateTime, nullable=True)
    checksum_validacao = db.Column(db.Text, nullable=True)  # Checksums geralmente são textos longos

    def __repr__(self):
        return '<Validacao %r>' % self.id_arquivo

class ExtratoOfx(db.Model):
    __tablename__ = 'extrato_ofx'
    id_arquivo = db.Column(db.Integer, db.ForeignKey('arquivo.id_arquivo'), primary_key=True, nullable=False)
    cod_banco = db.Column(db.Integer, db.ForeignKey('banco.cod_banco'), nullable=False)
    num_agencia_extrato = db.Column(db.Integer, nullable=True)
    num_conta_extrato = db.Column(db.Integer, nullable=True)
    data_inicial_extrato = db.Column(db.Date, nullable=True)
    data_final_extrato = db.Column(db.Date, nullable=True)
    saldo_inicial_extrato = db.Column(db.Float, nullable=True)
    saldo_final_extrato = db.Column(db.Float, nullable=True)
    id_arquivo_par = db.Column(db.Integer, nullable=True)
    data_verificacao_extrato = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return '<ExtratoOfx %r>' % self.id_arquivo