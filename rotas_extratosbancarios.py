from app import app, csrf, db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template,session, redirect,url_for,flash
from flask_login import current_user, login_required
from minio.error import S3Error
from minio_conf import minio_client,MINIO_BUCKET_NAME
from helpers import UploadFormExtrato
from models import ExtratoOfx, Arquivo, ExtratoPdf, Validacao,Banco
from datetime import datetime
import os
import fitz  # PyMuPDF
import ofxparse
import hashlib
import re
import io

@app.route('/extratosbancarios')
@login_required
def extratosbancarios():
    from models import Usuario
    form = UploadFormExtrato()
    form.banco.choices = [('','Selecione o Banco')] + [(m.cod_banco , m.nome_banco) for m in Banco.query.order_by(Banco.cod_banco.asc())]
    return render_template('extratosbancarios.html', titulo='GED - Extratos', form=form)

@app.route('/upload_file_extrato', methods=['POST'])
@login_required
def upload_file_extrato():
    form = UploadFormExtrato(request.form)
    print(form.banco.data)
    file_pdf = request.files.get('files_pdf')  # Arquivo PDF
    file_ofx = request.files.get('files_ofx')  # Arquivo OFX

    if not file_pdf or not file_ofx:
        flash("Ambos os arquivos PDF e OFX são necessários!", 'danger')
        return redirect(url_for('extratosbancarios'))

    try:
        # Informações do usuário logado
        usuario = current_user

        # Gerar hash SHA-256 para os arquivos
        pdf_hash = gerar_hash_sha256(file_pdf.stream)
        ofx_hash = gerar_hash_sha256(file_ofx.stream)

        # Salvar os arquivos localmente para processamento
        pdf_filename = f'{pdf_hash}.pdf'
        # pdf_filename = secure_filename(file_pdf.filename)
        ofx_filename = f'{ofx_hash}.ofx'
        # ofx_filename = secure_filename(file_ofx.filename)

        upload_folder = app.config['UPLOAD_PATH']
        os.makedirs(upload_folder, exist_ok=True)

        pdf_path = os.path.join(upload_folder, pdf_filename)
        ofx_path = os.path.join(upload_folder, ofx_filename)

        file_pdf.save(pdf_path)
        file_ofx.save(ofx_path)

        # Processar informações do PDF e OFX
        pdf_info = extract_pdf_info(pdf_path)
        with open(ofx_path, "r", encoding="latin-1") as ofx_file_obj:
            ofx_info = extract_ofx_info(ofx_file_obj)

        # Inserir no banco de dados e MinIO
        with db.session.begin_nested():
            # Registro na tabela Arquivo para PDF
            novo_arquivo_pdf = Arquivo(
                cnpj=usuario.cnpj,
                cpf=usuario.cpf,
                id_tipo_arquivo=3,  # Assumindo que 3 é PDF/A
                nome_arquivo=file_pdf.filename,
                data_hora_upload_arquivo=datetime.now(),
                tipo_arquivo='Extrato PDF/A',
                url_minio_arquivo=f"{MINIO_BUCKET_NAME}/{pdf_filename}",
            )
            db.session.add(novo_arquivo_pdf)
            db.session.flush()

            # Registro na tabela ExtratoPdf
            novo_extrato_pdf = ExtratoPdf(
                id_arquivo=novo_arquivo_pdf.id_arquivo,
                cod_banco=form.banco.data,
                num_agencia_extrato=pdf_info['agencia'],
                num_conta_extrato=pdf_info['conta'],
                data_inicial_extrato=pdf_info['data_inicial'],
                data_final_extrato=pdf_info['data_final'],
                saldo_inicial_extrato=pdf_info['saldo_inicial'],
                saldo_final_extrato=pdf_info['saldo_final']
            )
            db.session.add(novo_extrato_pdf)

            # Registro de validação do PDF
            validacao_pdf = Validacao(
                id_arquivo=novo_arquivo_pdf.id_arquivo,
                id_erro=1,
                status_validacao=True,
                data_hora_validacao=datetime.now(),
                checksum_validacao=pdf_hash
            )
            db.session.add(validacao_pdf)

            # Registro na tabela Arquivo para OFX
            novo_arquivo_ofx = Arquivo(
                cnpj=usuario.cnpj,
                cpf=usuario.cpf,
                id_tipo_arquivo=4,  # Assumindo que 2 é OFX
                nome_arquivo=file_ofx.filename,
                data_hora_upload_arquivo=datetime.now(),
                tipo_arquivo='Extrato OFX',
                url_minio_arquivo=f"{MINIO_BUCKET_NAME}/{ofx_filename}",
            )
            db.session.add(novo_arquivo_ofx)
            db.session.flush()

            # Registro na tabela ExtratoOfx
            novo_extrato_ofx = ExtratoOfx(
                id_arquivo=novo_arquivo_ofx.id_arquivo,
                cod_banco=ofx_info['cod_banco'],
                num_agencia_extrato=None,
                num_conta_extrato=ofx_info['conta'],
                data_inicial_extrato=ofx_info['data_inicial'],
                data_final_extrato=ofx_info['data_final'],
                saldo_inicial_extrato=None,
                saldo_final_extrato=ofx_info['saldo_final']
            )
            db.session.add(novo_extrato_ofx)

            # Registro de validação do OFX
            validacao_ofx = Validacao(
                id_arquivo=novo_arquivo_ofx.id_arquivo,
                id_erro=1,
                status_validacao=True,
                data_hora_validacao=datetime.now(),
                checksum_validacao=ofx_hash
            )
            db.session.add(validacao_ofx)

        # Upload dos arquivos para o MinIO
        minio_client.fput_object(
            MINIO_BUCKET_NAME,
            pdf_filename,
            pdf_path,
            content_type=file_pdf.mimetype,
            metadata={"integrity-hash": pdf_hash}  # Adiciona hash como metadado

        )
        minio_client.fput_object(
            MINIO_BUCKET_NAME,
            ofx_filename, 
            ofx_path,
            content_type=file_ofx.mimetype,
            metadata={"integrity-hash": ofx_hash}  # Adiciona hash como metadado
        )

        # Commit final no banco
        db.session.commit()

        # Remover arquivos temporários
        os.remove(pdf_path)
        os.remove(ofx_path)

        flash("Arquivos PDF e OFX processados e enviados com sucesso!", 'success')

    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))
        flash(f"Erro ao salvar no banco de dados: {str(e)}", 'danger')
    except Exception as e:
        flash(f"Erro inesperado: {str(e)}", 'danger')

    return redirect(url_for('extratosbancarios'))

@app.route('/processar', methods=['POST'])
@csrf.exempt
def processar():
    try:
        # print("Arquivos recebidos:", request.files)  # Log dos arquivos enviados
        pdf_file = request.files.get('pdf')
        # print(pdf_file)
        ofx_file = request.files.get('ofx')
        # print(ofx_file)

        if not pdf_file or not ofx_file:
            print("Arquivos ausentes")
            return jsonify({"error": "Ambos os arquivos PDF e OFX são necessários."}), 400

        saldo_pdf = extrair_saldo_conta_corrente_pdf(pdf_file)
        saldo_ofx = calcular_saldo_total_ofx(ofx_file)
        print(f"Saldo PDF: {saldo_pdf}, Saldo OFX: {saldo_ofx}")

        iguais = abs(saldo_pdf - saldo_ofx) < 0.01

        return jsonify({
            "saldo_pdf": saldo_pdf,
            "saldo_ofx": saldo_ofx,
            "iguais": iguais
        })
    except Exception as e:
        print("Erro:", str(e))
        return jsonify({"error": str(e)}), 400



def extrair_saldo_conta_corrente_pdf(pdf_file):
    # Abra o PDF usando o fluxo de dados
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf:
        for pagina in pdf:
            texto = pagina.get_text()
            linhas = texto.splitlines()
            for i, linha in enumerate(linhas):
                if "Saldo final do período" in linha:
                    if i + 1 < len(linhas):  # Pegar a linha seguinte
                        valor = linhas[i + 2].strip()
                        return float(valor.replace("R$", "").replace(".", "").replace(",", "."))
                if "Saldo de conta corrente" in linha:
                    if i + 1 < len(linhas):  # Pegar a linha seguinte
                        valor = linhas[i + 1].strip()
                        return float(valor.replace("R$", "").replace(".", "").replace(",", "."))
    raise ValueError("Saldo de conta corrente não encontrado no PDF.")

def calcular_saldo_total_ofx(ofx_file):
    # Use o fluxo do arquivo diretamente
    ofx = ofxparse.OfxParser.parse(ofx_file)
    saldo_final = float(ofx.account.statement.balance)
    return saldo_final

def extract_ofx_info(file_stream):
    """
    Extrai informações bancárias de um arquivo OFX.
    
    Parâmetros:
    - file_stream: Objeto do arquivo OFX (deve ser aberto no modo leitura ou bytes).
    
    Retorno:
    - Um dicionário com as informações extraídas.
    """
    try:
        # # Garantir que o arquivo seja seekable, criando um buffer se necessário
        # if isinstance(file_stream, (str, bytes)):
        #     file_stream = io.StringIO(file_stream)  # Buffer para texto
        # elif not hasattr(file_stream, "seek"):
        #     file_stream = io.StringIO(file_stream.read())  # Transformar em buffer

        # Fazer o parse do arquivo OFX
        ofx = ofxparse.OfxParser.parse(file_stream)

        # Extrair as informações bancárias
        info = {
            "cod_banco": int(ofx.account.routing_number),
            "conta": ofx.account.number,
            "data_inicial": ofx.account.statement.start_date,
            "data_final": ofx.account.statement.end_date,
            "saldo_final": float(ofx.account.statement.balance)
        }
        print(info)
        return info

    except Exception as e:
        raise ValueError(f"Erro ao processar o arquivo OFX: {str(e)}")

def extract_pdf_info(file_path):
    """
    Extrai informações do PDF e organiza em um dicionário.

    :param file_path: Caminho para o arquivo PDF.
    :return: Dicionário com as informações extraídas.
    """
    try:
        with fitz.open(file_path) as pdf_document:  # Abre o PDF com 'with'
            # Concatena texto de todas as páginas
            full_text = ""
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                full_text += page.get_text()
            
            if 'Nu Pagamentos' in full_text:
                agencia_conta_match = re.search(r"Agência\s*Conta\s*([\d\-]+)", full_text)
                agencia_conta = agencia_conta_match.group(1) if agencia_conta_match else None
                print(agencia_conta)
                # Mapeamento dos meses em português
                meses = {
                    "JANEIRO": 1, "FEVEREIRO": 2, "MARÇO": 3, "ABRIL": 4, "MAIO": 5, "JUNHO": 6,
                    "JULHO": 7, "AGOSTO": 8, "SETEMBRO": 9, "OUTUBRO": 10, "NOVEMBRO": 11, "DEZEMBRO": 12
                }

                # Expressão regular para capturar datas no formato "01 DE NOVEMBRO DE 2024"
                datas_matches = re.findall(r"(\d{2})\s+DE\s+(\w+)\s+DE\s+(\d{4})", full_text)

                # Converter as datas para objetos datetime
                datas_convertidas = []
                for match in datas_matches:
                    dia, mes, ano = match
                    mes_numero = meses.get(mes.upper(), 0)  # Obtém o número do mês
                    if mes_numero:
                        data = datetime(int(ano), mes_numero, int(dia))
                        datas_convertidas.append(data)
                datas = list(set(datas_convertidas))
                data_inicial = datas[0]
                data_final = datas[1]
                # Capturar saldo inicial
                saldo_inicial_match = re.search(r"R\$\s*([-\d.,]+)\s*Saldo inicial", full_text)
                saldo_inicial = saldo_inicial_match.group(1) if saldo_inicial_match else None
                print(saldo_inicial)
                # Capturar saldo final
                saldo_final_match = re.search(r"Saldo final do período\s*([\d.,]+)", full_text)
                saldo_final = saldo_final_match.group(1) if saldo_final_match else None
                print(saldo_final)

                # Verifica se os dados foram encontrados e organiza em um dicionário
                pdf_info = {
                    "agencia": agencia_conta if agencia_conta else None,
                    "conta": agencia_conta if agencia_conta else None,
                    "data_inicial": data_inicial,
                    "data_final": data_final,
                    "saldo_inicial": saldo_inicial if saldo_inicial else None,
                    "saldo_final": saldo_final if saldo_final else None,
                }
            else:
                # Expressões regulares para capturar informações específicas
                agencia_conta_match = re.search(r"Agência e Conta:\s*(\d+)\s*/\s*(\d+[-]?\d*)", full_text)
                periodo_match = re.search(r"Período:\s*([\d/]+)\s*a\s*([\d/]+)", full_text)
                saldo_inicial_match = re.search(r"Saldo anterior.*?Saldo \(R\$\)\s*([-\d.,]+)", full_text, re.DOTALL)
                saldo_inicial = saldo_inicial_match.group(1) if saldo_inicial_match else None
                # Saldo final: Busca pelo contexto "Saldo de conta corrente"
                saldo_final_match = re.findall(r"Saldo de conta corrente.*?([-\d.,]+)", full_text, re.DOTALL)
                saldo_final = saldo_final_match[-1] if saldo_final_match else None  # Pega o último valor encontrado

                # Converter o saldo para float
                if saldo_inicial:
                    try:
                        # Remover símbolos de moeda e formatar
                        saldo_inicial = float(saldo_inicial.replace("R$", "").replace(",", ".").replace(".", "", saldo_inicial[:-3].count(".")))
                    except ValueError:
                        raise ValueError(f"Saldo inválido encontrado: {saldo_inicial}")
                else:
                    saldo_inicial = None  # Caso não exista saldo capturado
                    
                # Converter o saldo para float
                if saldo_final:
                    try:
                        # Remover símbolos de moeda e formatar
                        saldo_final = float(saldo_final.replace("R$", "").replace(",", ".").replace(".", "", saldo_final[:-3].count(".")))
                    except ValueError:
                        raise ValueError(f"Saldo inválido encontrado: {saldo_final}")
                else:
                    saldo_final = None  # Caso não exista saldo capturado
                
                # Verifica se os dados foram encontrados e organiza em um dicionário
                pdf_info = {
                    "agencia": agencia_conta_match.group(1) if agencia_conta_match else None,
                    "conta": agencia_conta_match.group(2) if agencia_conta_match else None,
                    "data_inicial": periodo_match.group(1) if periodo_match else None,
                    "data_final": periodo_match.group(2) if periodo_match else None,
                    "saldo_inicial": saldo_inicial if saldo_inicial else None,
                    "saldo_final": saldo_final if saldo_final else None,
                }

            print(pdf_info)
            return pdf_info

    except Exception as e:
        print(f"Ocorreu um erro ao processar o PDF: {e}")
        return None

def gerar_hash_sha256(file_stream):
    """Gera um hash SHA-256 com base no conteúdo do arquivo."""
    sha256 = hashlib.sha256()
    for chunk in iter(lambda: file_stream.read(4096), b""):  # Lê o arquivo em blocos
        sha256.update(chunk)
    file_stream.seek(0)  # Reinicia o ponteiro do arquivo após leitura
    return sha256.hexdigest()