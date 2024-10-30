import mysql.connector
from mysql.connector import errorcode
from env.credenciais import servidor_cred,usuario_cred,senha_cred

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

    cursor.execute("CREATE DATABASE `ged_contabilidade`;")

    cursor.execute("USE `ged_contabilidade`;")

    # # # criando tabelas # #
    # TABLES = {}

    # TABLES['TipoNF'] = ('''
    # CREATE TABLE TipoNF (
    # idTipoNF INT UNSIGNED NOT NULL AUTO_INCREMENT,
    # descricaoNF VARCHAR(255) NULL,
    # modeloNF INT UNSIGNED NULL,
    # PRIMARY KEY(idTipoNF)
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

    # TABLES['TipoErro'] = ('''
    #     CREATE TABLE TipoErro (
    #     idErro INT UNSIGNED NOT NULL AUTO_INCREMENT,
    #     descricaoErro VARCHAR(255) NULL,
    #     PRIMARY KEY(idErro)
    #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

    # TABLES['TipoArquivo'] = ('''
    #     CREATE TABLE TipoArquivo (
    #     idTipoArquivo INT UNSIGNED NOT NULL AUTO_INCREMENT,
    #     descricaoArquivo VARCHAR(255) NULL,
    #     PRIMARY KEY(idTipoArquivo)
    #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

    # TABLES['Bancos'] = ('''
    #     CREATE TABLE Bancos (
    #     codBanco INT UNSIGNED NOT NULL AUTO_INCREMENT,
    #     nomeBanco VARCHAR(255) NULL,
    #     PRIMARY KEY(codBanco)
    #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

    # TABLES['Cliente'] = ('''
    #     CREATE TABLE Cliente (
    #     cpf_cnpj BIGINT UNSIGNED NOT NULL,
    #     nomeCliente VARCHAR(255) NULL,
    #     telefoneCliente BIGINT UNSIGNED NULL,
    #     enderecoCliente TEXT NULL,
    #     emailCliente VARCHAR(255) NULL,
    #     senhaCliente TEXT NULL,
    #     ultimoLoginCliente DATE NULL,
    #     PRIMARY KEY(cpf_cnpj)
    #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

    # TABLES['Arquivo'] = ('''
    #     CREATE TABLE Arquivo (
    #     idArquivo INT UNSIGNED NOT NULL AUTO_INCREMENT,
    #     idTipoArquivo INT UNSIGNED NOT NULL,
    #     cpf_cnpj BIGINT UNSIGNED NOT NULL,
    #     nomeArquivo VARCHAR(255) NULL,
    #     datahoraUploadArquivo DATETIME NULL,
    #     tipoArquivo VARCHAR(255) NULL,
    #     urlMinioArquivo TEXT NULL,
    #     PRIMARY KEY(idArquivo),
    #     FOREIGN KEY(cpf_cnpj)
    #         REFERENCES Cliente(cpf_cnpj)
    #         ON DELETE NO ACTION
    #         ON UPDATE NO ACTION,
    #     FOREIGN KEY(idTipoArquivo)
    #         REFERENCES TipoArquivo(idTipoArquivo)
    #         ON DELETE NO ACTION
    #         ON UPDATE NO ACTION
    #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

    # TABLES['NotaFiscal'] = ('''
    #     CREATE TABLE NotaFiscal (
    #     idTipoNF INT UNSIGNED NOT NULL,
    #     idArquivo INT UNSIGNED NOT NULL,
    #     numNota INT UNSIGNED NULL,
    #     dataEmissaoNota DATE NULL,
    #     valorNota FLOAT NULL,
    #     cnpjEmitenteNota BIGINT UNSIGNED NULL,
    #     cnpjDestinatarioNota BIGINT UNSIGNED NULL,
    #     notaVerificada BOOL NULL,
    #     dataVerificacaoNota DATE NULL,
    #     PRIMARY KEY(idArquivo),
    #     FOREIGN KEY(idArquivo)
    #         REFERENCES Arquivo(idArquivo)
    #         ON DELETE NO ACTION
    #         ON UPDATE NO ACTION,
    #     FOREIGN KEY(idTipoNF)
    #         REFERENCES TipoNF(idTipoNF)
    #         ON DELETE NO ACTION
    #         ON UPDATE NO ACTION
    #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

    # TABLES['ExtratoPdf'] = ('''
    #     CREATE TABLE ExtratoPdf (
    #     codBanco INT UNSIGNED NOT NULL,
    #     idArquivo INT UNSIGNED NOT NULL,
    #     numAgenciaExtrato INT UNSIGNED NULL,
    #     numContaExtrato INT UNSIGNED NULL,
    #     dataInicialExtrato DATE NULL,
    #     dataFinalExtrato DATE NULL,
    #     saldoInicialExtrato FLOAT NULL,
    #     saldoFinalExtrato FLOAT NULL,
    #     idArquivoPar INT UNSIGNED NULL,
    #     dataVerificacaoExtrato DATE NULL,
    #     PRIMARY KEY(idArquivo),
    #     FOREIGN KEY(idArquivo)
    #         REFERENCES Arquivo(idArquivo)
    #         ON DELETE NO ACTION
    #         ON UPDATE NO ACTION,
    #     FOREIGN KEY(codBanco)
    #         REFERENCES Bancos(codBanco)
    #         ON DELETE NO ACTION
    #         ON UPDATE NO ACTION
    #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

    # TABLES['Validacao'] = ('''
    #     CREATE TABLE Validacao (
    #     idArquivo INT UNSIGNED NOT NULL,
    #     idErro INT UNSIGNED NOT NULL,
    #     statusValidacao BOOL NULL,
    #     datahoraValidacao DATETIME NULL,
    #     checksumValidacao TEXT NULL,
    #     PRIMARY KEY(idArquivo),
    #     FOREIGN KEY(idArquivo)
    #         REFERENCES Arquivo(idArquivo)
    #         ON DELETE NO ACTION
    #         ON UPDATE NO ACTION,
    #     FOREIGN KEY(idErro)
    #         REFERENCES TipoErro(idErro)
    #         ON DELETE NO ACTION
    #         ON UPDATE NO ACTION
    #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

    # TABLES['ExtratoOfx'] = ('''
    #     CREATE TABLE ExtratoOfx (
    #     idArquivo INT UNSIGNED NOT NULL,
    #     codBanco INT UNSIGNED NOT NULL,
    #     numAgenciaExtrato INT UNSIGNED NULL,
    #     numContaExtrato INT UNSIGNED NULL,
    #     dataInicialExtrato DATE NULL,
    #     dataFinalExtrato DATE NULL,
    #     saldoInicialExtrato FLOAT NULL,
    #     saldoFinalExtrato FLOAT NULL,
    #     idArquivoPar INT UNSIGNED NULL,
    #     dataVerificacaoExtrato DATE NULL,
    #     PRIMARY KEY(idArquivo),
    #     FOREIGN KEY(idArquivo)
    #         REFERENCES Arquivo(idArquivo)
    #         ON DELETE NO ACTION
    #         ON UPDATE NO ACTION,
    #     FOREIGN KEY(codBanco)
    #         REFERENCES Bancos(codBanco)
    #         ON DELETE NO ACTION
    #         ON UPDATE NO ACTION
    #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')


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

    # commitando se não nada tem efeito
    conn.commit()

    cursor.close()
    conn.close()
