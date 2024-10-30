import os
from env.credenciais import SECRET_KEY_cred,SGBD_cred,usuario_cred,senha_cred,servidor_cred,database_cred

SECRET_KEY = SECRET_KEY_cred

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = SGBD_cred,
        usuario = usuario_cred,
        senha = senha_cred,
        servidor = servidor_cred,
        database = database_cred
    )

SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/upload'
