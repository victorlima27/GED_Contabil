# Projeto de TCC - Segurança da Informação na Prestação de Serviços Contábeis

## Descrição

Este projeto tem como objetivo desenvolver uma plataforma de Gestão Eletrônica de Documentos (GED) que garanta a troca segura de informações entre contabilidades e clientes, assegurando a integridade, disponibilidade e segurança da informação. O sistema permite o upload, download e alterações de arquivos em tempo real, priorizando a segurança dos dados sensíveis.

## Funcionalidades

- **Upload de Documentos:** Os usuários podem enviar documentos para a plataforma de forma segura.
- **Download de Documentos:** Possibilidade de download dos documentos armazenados.
- **Listagem de Arquivos:** Visualização dos arquivos disponíveis na plataforma.
- **Segurança da Informação:** Implementação de boas práticas de segurança, incluindo controle de acesso, criptografia e verificação de integridade.

## Segurança Implementada

- **Hashing:** Utilizaremos funções hash (como SHA-256) para garantir a integridade dos arquivos. Isso permitirá verificar se os arquivos foram alterados ou corrompidos durante o armazenamento ou a transferência.
- **Criptografia:** Dados sensíveis serão criptografados para proteger a confidencialidade das informações trocadas entre os usuários e o sistema.
- **Controle de Acesso:** Implementaremos autenticação e autorização para garantir que apenas usuários autorizados possam acessar ou modificar os documentos.

## Tecnologias Utilizadas

- **Python:** Linguagem de programação principal.
- **Flask:** Framework web para a construção da API.
- **MinIO:** Solução de armazenamento compatível com S3 para gerenciamento de arquivos.
- **SQL (MySQL):** Banco de dados para armazenamento de informações.
- **Swagger:** Ferramenta para documentação da API.

## Instalação

### Pré-requisitos

- Python 3.x
- Pip
- MinIO
- MySQL (ou outro banco de dados de sua preferência)

### Passo a Passo

1. Clone o repositório:
   ```bash
   https://github.com/victorlima27/GED_Contabil.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd GED_Contabil
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configuração MinIO (Windows):
   ```bash
   Invoke-WebRequest -Uri "https://dl.min.io/server/minio/release/windows-amd64/minio.exe" -OutFile .\MINIO\minio.exe
   .\MINIO\minio.exe server .\MINIO --console-address ":9001"
   ```
   - Certifique-se de que o MinIO está em execução e crie um bucket para armazenar os documentos.
5. Execute a aplicação:
   ```bash
   python start.py
   ```
