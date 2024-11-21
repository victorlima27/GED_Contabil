from flask import Flask, request, jsonify, render_template,session, redirect,url_for,flash
from minio.error import S3Error
from helpers import UploadForm
from flask_login import current_user, login_required
from app import app
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from minio_conf import minio_client,MINIO_BUCKET_NAME
import fitz  # PyMuPDF

@app.route('/notasfiscais')
@login_required
def notasfiscais():
    from models import Usuario
    form = UploadForm()  # Instancia o formulário
    text_page = ''
    return render_template('notasfiscais.html', titulo='GED - Carregamentos', text_page=text_page, form=form)

@app.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    form = UploadForm(request.form)
    files = request.files.getlist('files')  # Lista de arquivos enviados
    for file in files:
        try:
            filename = secure_filename(file.filename)  # Nome seguro
            if not filename.endswith(('.pdf', '.xml')):
                flash(f"Arquivo '{filename}' não é permitido. Apenas PDF e XML!", 'danger')
                continue

            # Certifique-se de que o diretório de upload exista
            upload_folder = app.config['UPLOAD_PATH']
            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
           
            numero_nota = extrair_numero_nota(file_path)
            if numero_nota:
                print(f"Número da Nota Fiscal: {numero_nota}")
            else:
                print("Número da Nota Fiscal não encontrado.")

            # Upload para o MinIO
            minio_client.fput_object(
                MINIO_BUCKET_NAME,  # Nome do bucket
                filename,  # Nome do arquivo no bucket
                file_path,  # Caminho do arquivo local
                content_type=file.mimetype  # Tipo MIME
            )

            flash(f"Arquivo '{filename}' enviado com sucesso para o MinIO!", 'success')
            os.remove(file_path)  # Remover arquivo temporário

        except S3Error as e:
            flash(f"Erro ao enviar '{filename}': {str(e)}", 'danger')
        except Exception as e:
            flash(f"Erro inesperado com '{filename}': {str(e)}", 'danger')

    return redirect('/notasfiscais')

def extrair_numero_nota(pdf_path):
    # Abrir o PDF
    with fitz.open(pdf_path) as pdf:
        for page in pdf:  # Iterar por todas as páginas (se necessário)
            # Extrair texto completo
            text = page.get_text()

            # Procurar pelo padrão "Número da Nota" e extrair o número subsequente
            if "Número da Nota" in text:
                lines = text.splitlines()
                for i, line in enumerate(lines):
                    if "Número da Nota" in line:
                        # O número está na linha seguinte
                        numero_nota = lines[i + 1].strip()
                        return numero_nota  # Retornar o número da nota

    return None  # Retornar None se o número não for encontrado

@app.route('/list_files')
def list_files():
    objects = minio_client.list_objects(MINIO_BUCKET_NAME)
    files = [obj.object_name for obj in objects]
    return render_template('list_files.html', files=files)