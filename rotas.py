from flask import Flask, request, jsonify, render_template,session, redirect,url_for,flash
from minio.error import S3Error
from helpers import UploadForm
from flask_login import current_user, login_required
from app import app
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from minio_conf import minio_client,MINIO_BUCKET_NAME

@app.route('/')
@login_required
def home():
    from models import Usuario
    user = Usuario.query.filter_by(cpf=current_user.cpf).first()
    text_page = 'INÍCIO'
    momento = datetime.now().strftime("%H:%M")
    return render_template('home.html', titulo='GED - Home', text_page=text_page)

@app.route('/carregamentos')
@login_required
def carregamentos():
    from models import Usuario
    user = Usuario.query.filter_by(cpf=current_user.cpf).first()
    text_page = 'CARREGAMENTOS'
    momento = datetime.now().strftime("%H:%M")
    return render_template('carregamentos.html', titulo='GED - Carregamentos', text_page=text_page)

