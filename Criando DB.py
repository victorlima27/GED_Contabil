import mysql.connector
from mysql.connector import errorcode
from env.credenciais import servidor_cred,usuario_cred,senha_cred
from flask_bcrypt import generate_password_hash
import datetime

print("Conectando...")
escolha = input(str("Deseja iniciar o prepara_banco ?"))
if escolha == 'sim' or escolha == 's':
    try:
        conn = mysql.connector.connect(
            host= servidor_cred,
            user= usuario_cred,
            password= senha_cred
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
        else:
            print(err)

    cursor = conn.cursor()

    # cursor.execute("DROP DATABASE IF EXISTS `ged_contabilidade`;")

    # cursor.execute("CREATE DATABASE `ged_contabilidade`;")

    cursor.execute("USE `ged_contabilidade`;")

    # for tabela_nome in TABLES:
    #     tabela_sql = TABLES[tabela_nome]
    #     try:
    #         print('Criando tabela {}:'.format(tabela_nome), end=' ')
    #         cursor.execute(tabela_sql)
    #     except mysql.connector.Error as err:
    #         if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
    #             print('Já existe')
    #         else:
    #             print(err.msg)
    #     else:
    #         print('OK')

    # Inserindo Empresa
    empresa_sql = 'INSERT INTO empresa (cnpj, razao_social_empresa, email_empresa, telefone_empresa, tributacao_empresa) VALUES (%s, %s, %s, %s, %s)'

    empresas = [
        ('102760847000162', 'Empresa Teste', 'victor.lima@gedcontabil.loca', '2730387700', 'Simples Nacional'),
    ]

    cursor.executemany(empresa_sql, empresas)

    cursor.execute('SELECT * FROM ged_contabilidade.empresa')
    print(' -------------  Empresas:  -------------')
    for empresa in cursor.fetchall():
        print(empresa[1])

    # Commitando para que as inserções tenham efeito
    conn.commit()

    # Inserindo Usuarios
    usuario_sql = 'INSERT INTO usuario (cpf, cnpj, nome_usuario, telefone_usuario, email_usuario, senha_usuario, ultimo_login_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    usuarios = [
        ('12345678912', '102760847000162', 'Usuário Teste', '27999999999', 'teste@teste.com.br', generate_password_hash('123456').decode('utf-8'), datetime.date.today()),
    ]

    cursor.executemany(usuario_sql, usuarios)

    cursor.execute('SELECT * FROM ged_contabilidade.usuario')
    print(' -------------  Usuários:  -------------')
    for usuario in cursor.fetchall():
        print(usuario[2])  # Exibe o nome do usuário

    # Commitando para que as inserções tenham efeito
    conn.commit()


    cursor.close()
    conn.close()
