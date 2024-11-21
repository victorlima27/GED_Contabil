from flask import Flask, request, jsonify, render_template,session, redirect,url_for,flash,send_file
from minio.error import S3Error
from flask_login import current_user, login_required
from app import app,db, gerar_hash_sha256
from models import  Arquivo,Validacao,TipoArquivo
from werkzeug.utils import secure_filename
from datetime import datetime
from minio_conf import minio_client,MINIO_BUCKET_NAME

@app.route('/documentos')
@login_required
def documentos():
    from models import Arquivo,Validacao
    documentos = (
        db.session.query(
            Arquivo.id_arquivo,
            Arquivo.nome_arquivo,
            Arquivo.tipo_arquivo,
            Arquivo.data_hora_upload_arquivo,
            Validacao.status_validacao,
            Validacao.id_erro
        )
        .outerjoin(Validacao, Arquivo.id_arquivo == Validacao.id_arquivo)
        .all()
    )
    # Converter os resultados para uma lista de dicionários
    documentos_data = []
    for doc in documentos:
        documentos_data.append({
            "id_arquivo": doc.id_arquivo,
            "nome_arquivo": doc.nome_arquivo,
            "tipo_arquivo": doc.tipo_arquivo,
            "data_hora_upload_arquivo": doc.data_hora_upload_arquivo,
            "status_validacao": doc.status_validacao,
            "id_erro": doc.id_erro,
            "tem_erro": doc.id_erro != 1  # Determina se tem erro
        })

    dat = datetime
    return render_template('documentos.html', titulo='GED - Extratos', dat=dat, documentos=documentos_data)

@app.route('/download_file/<int:id_arquivo>', methods=['GET'])
@login_required
def download_file(id_arquivo):
    arquivo = (
        db.session
        .query(
            Arquivo.id_arquivo,
            Arquivo.url_minio_arquivo,
            Validacao.checksum_validacao,
            TipoArquivo.descricao_arquivo
        )
        .outerjoin(Validacao, Arquivo.id_arquivo == Validacao.id_arquivo)
        .outerjoin(TipoArquivo, Arquivo.id_tipo_arquivo == TipoArquivo.id_tipo_arquivo)
        .filter(Arquivo.id_arquivo == id_arquivo) # Corrigido: Usando filter em vez de filter_by
        .first()
    )
    filename = arquivo.url_minio_arquivo.replace('gedcontabilidade/','')
    if not filename:
        return "Arquivo não especificado.", 400

    try:
        # Obter informações do arquivo no MinIO
        obj = minio_client.stat_object(MINIO_BUCKET_NAME, filename)

        # Recuperar o hash do metadado
        stored_hash = obj.metadata.get("X-Amz-Meta-Integrity-Hash")  # Hash armazenado no metadado

        # Fazer download do arquivo
        file_data = minio_client.get_object(MINIO_BUCKET_NAME, filename)
        # Comparar os hashes
        if stored_hash != arquivo.checksum_validacao:
            return "Falha na integridade do arquivo! O arquivo foi alterado.", 400

        # Retornar o arquivo se os hashes forem iguais
        return send_file(file_data, download_name=filename)

    except S3Error as e:
        return f"Erro ao baixar arquivo: {str(e)}", 500
