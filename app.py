from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flasgger import Swagger
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

# # Configuração para E-mail se Necessário # #
# app.config['MAIL_SERVER'] = 'x.x.x.x.'  # Use o servidor de e-mail apropriado
# app.config['MAIL_PORT'] = 587  # Use a porta correta para envio de e-mails
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'nome.sobrenome@dominio'
# app.config['MAIL_PASSWORD'] = 'password'
# app.config['MAIL_DEFAULT_SENDER'] = 'nome.sobrenome@dominio'  # Defina o remetente aqui

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
swagger = Swagger(app)
login_manager = LoginManager()
migrate = Migrate(app,db)



# Importe suas rotas
from rotas_notasfiscais import *
from rotas_extratosbancarios import *
from rotas_documentos import *
from rotas import *
from users import *



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
