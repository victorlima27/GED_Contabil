from flask import Flask, request, jsonify
from minio import Minio
from minio.error import S3Error
from app import app

# Inicializa o cliente MinIO
minio_client = Minio(
    "127.0.0.1:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload um arquivo para o MinIO.
    ---
    parameters:
      - name: file
        type: file
        required: true
        description: O arquivo a ser enviado.
    responses:
      200:
        description: Arquivo enviado com sucesso!
      400:
        description: Erro ao enviar o arquivo.
    """
    file = request.files['file']
    minio_client.put_object(
        "seu-bucket",
        file.filename,
        file,
        file.content_length
    )
    return jsonify({"message": "Arquivo enviado com sucesso!"}), 200

@app.route('/files', methods=['GET'])
def list_files():
    """
    Lista todos os arquivos armazenados no MinIO.
    ---
    responses:
      200:
        description: Lista de arquivos.
      404:
        description: Nenhum arquivo encontrado.
    """
    objects = minio_client.list_objects("seu-bucket", recursive=True)
    file_list = [obj.object_name for obj in objects]
    return jsonify(file_list), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    Faz o download de um arquivo do MinIO.
    ---
    parameters:
      - name: filename
        type: string
        required: true
        description: Nome do arquivo a ser baixado.
    responses:
      200:
        description: Arquivo baixado com sucesso.
      404:
        description: Arquivo não encontrado.
    """
    try:
        data = minio_client.get_object("seu-bucket", filename)
        return data.read(), 200
    except S3Error as e:
        return jsonify({"error": str(e)}), 404
