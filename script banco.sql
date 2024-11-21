TABLES['Observações'] = ('''
CREATE TABLE TipoNF (
  idTipoNF INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  descricaoNF VARCHAR NULL,
  modeloNF INTEGER UNSIGNED NULL,
  PRIMARY KEY(idTipoNF)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

TABLES['Observações'] = ('''
CREATE TABLE TipoErro (
  idErro INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  decricaoErro VARCHAR NULL,
  PRIMARY KEY(idErro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

TABLES['Observações'] = ('''
CREATE TABLE TipoArquivo (
  idTipoArquivo INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  descricaoArquivo VARCHAR NULL,
  PRIMARY KEY(idTipoArquivo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

TABLES['Observações'] = ('''
CREATE TABLE Bancos (
  codbanco INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  nomeBanco VARCHAR NULL,
  PRIMARY KEY(codbanco)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

TABLES['Observações'] = ('''
CREATE TABLE Cliente (
  CPF/CNPJ INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  nomeCliente VARCHAR NULL,
  telefoneCliente INTEGER UNSIGNED NULL,
  enderecoCliente TEXT NULL,
  emailCliente TEXT NULL,
  senhaCliente TEXT NULL,
  ultimoLoginCliente DATE NULL,
  PRIMARY KEY(CPF/CNPJ)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

TABLES['Observações'] = ('''
CREATE TABLE Arquivo (
  idArquivo INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  idTipoArquivo INTEGER UNSIGNED NOT NULL,
  CPF/CNPJ INTEGER UNSIGNED NOT NULL,
  nomeArquivo VARCHAR NULL,
  datahoraUploadArquivo DATETIME NULL,
  tipoArquivo VARCHAR NULL,
  urlMinioArquivo TEXT NULL,
  PRIMARY KEY(idArquivo),
  FOREIGN KEY(CPF/CNPJ)
    REFERENCES Cliente(CPF/CNPJ)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(idTipoArquivo)
    REFERENCES TipoArquivo(idTipoArquivo)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

TABLES['Observações'] = ('''
CREATE TABLE NotaFiscal (
  idTipoNF INTEGER UNSIGNED NOT NULL,
  idArquivo INTEGER UNSIGNED NOT NULL,
  numNota INTEGER UNSIGNED NULL,
  dataEmissaoNota DATE NULL,
  valorNota FLOAT NULL,
  cnpjEmitenteNota INTEGER UNSIGNED NULL,
  cnpjDestinatarioNota INTEGER UNSIGNED NULL,
  notaVerificada BOOL NULL,
  dataVerificacaoNota DATE NULL,
  PRIMARY KEY(idArquivo),
  FOREIGN KEY(idArquivo)
    REFERENCES Arquivo(idArquivo)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(idTipoNF)
    REFERENCES TipoNF(idTipoNF)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

TABLES['Observações'] = ('''
CREATE TABLE ExtratoPdf (
  codbanco INTEGER UNSIGNED NOT NULL,
  idArquivo INTEGER UNSIGNED NOT NULL,
  numAgenciaExtrato INTEGER UNSIGNED NULL,
  numContaExtrato INTEGER UNSIGNED NULL,
  dataInicialExtrato DATE NULL,
  dataFinalExtrato DATE NULL,
  saldoInicialExtrato FLOAT NULL,
  saldoFinalExtrato FLOAT NULL,
  idArquivoPar INTEGER UNSIGNED NULL,
  dataVerificacaoExtrato DATE NULL,
  PRIMARY KEY(idArquivo),
  FOREIGN KEY(idArquivo)
    REFERENCES Arquivo(idArquivo)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(codbanco)
    REFERENCES Bancos(codbanco)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

TABLES['Observações'] = ('''
CREATE TABLE Validacao (
  idArquivo INTEGER UNSIGNED NOT NULL,
  idErro INTEGER UNSIGNED NOT NULL,
  statusValidacao BOOL NULL,
  datahoraValidacao DATETIME NULL,
  checksumValidacao TEXT NULL,
  PRIMARY KEY(idArquivo),
  FOREIGN KEY(idArquivo)
    REFERENCES Arquivo(idArquivo)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(idErro)
    REFERENCES TipoErro(idErro)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')

TABLES['Observações'] = ('''
CREATE TABLE ExtratoOfx (
  idArquivo INTEGER UNSIGNED NOT NULL,
  codbanco INTEGER UNSIGNED NOT NULL,
  numAgenciaExtrato INTEGER UNSIGNED NULL,
  numContaExtrato INTEGER UNSIGNED NULL,
  dataInicialExtrato DATE NULL,
  dataFinalExtrato DATE NULL,
  saldoInicialExtrato FLOAT NULL,
  saldoFinalExtrato FLOAT NULL,
  idArquivoPar INTEGER UNSIGNED NULL,
  dataVerificacaoExtrato DATE NULL,
  PRIMARY KEY(idArquivo),
  FOREIGN KEY(idArquivo)
    REFERENCES Arquivo(idArquivo)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(codbanco)
    REFERENCES Bancos(codbanco)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ''')


