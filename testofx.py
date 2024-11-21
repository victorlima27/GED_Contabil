import ofxparse
import fitz
import os
import re
import io
from datetime import datetime

uplod_folder = os.path.dirname(os.path.abspath(__file__)) + '/upload'
# def calcular_saldo_ofx(caminho_ofx):
#     with open(caminho_ofx, 'r', encoding='latin-1') as ofx_file:
#         ofx = ofxparse.OfxParser.parse(ofx_file)

#     # Tentar acessar o saldo inicial
#     statement = ofx.account.statement
#     saldo_inicial = getattr(statement, 'start_balance', 0)  # Usa 0 como fallback se não encontrar

#     # Calcular saldo com base nas transações
#     transacoes = statement.transactions
#     saldo_calculado = saldo_inicial + sum(tx.amount for tx in transacoes)

#     return saldo_inicial, saldo_calculado

# # Exemplo de uso
# caminho_ofx = r"C:\Users\Victão\Downloads\extratoCC.ofx"
# saldo_inicial, saldo_calculado = calcular_saldo_ofx(caminho_ofx)
# print(f"Saldo Inicial: R$ {saldo_inicial:.2f}")
# print(f"Saldo Calculado: R$ {saldo_calculado:.2f}")

# # Ler o arquivo OFX
# def extrair_valor_final_ofx(caminho_ofx):
#     with open(caminho_ofx, 'r', encoding='latin-1') as ofx_file:
#         ofx = ofxparse.OfxParser.parse(ofx_file)

#     # Extrair o saldo final
#     saldo_final = ofx.account.statement.balance
#     return saldo_final
# saldo_final_ofx = extrair_valor_final_ofx(caminho_ofx)
# print(f"Saldo final do arquivo OFX: R$ {saldo_final_ofx:.2f}")

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
            # print(full_text)
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
                # Saldo final: Busca pelo contexto "Saldo de conta corrente"
                saldo_final_match = re.findall(r"Saldo de conta corrente.*?([-\d.,]+)", full_text, re.DOTALL)
                saldo_final = saldo_final_match[-1] if saldo_final_match else None  # Pega o último valor encontrado

            
                # Verifica se os dados foram encontrados e organiza em um dicionário
                pdf_info = {
                    "agencia": agencia_conta_match.group(1) if agencia_conta_match else None,
                    "conta": agencia_conta_match.group(2) if agencia_conta_match else None,
                    "data_inicial": periodo_match.group(1) if periodo_match else None,
                    "data_final": periodo_match.group(2) if periodo_match else None,
                    "saldo_inicial": saldo_inicial_match.group(1) if saldo_inicial_match else None,
                    "saldo_final": saldo_final if saldo_final else None,
                }
            print(pdf_info)
            return pdf_info

    except Exception as e:
        print(f"Ocorreu um erro ao processar o PDF: {e}")
        return None

# Exemplo de uso
file_path = os.path.join(uplod_folder,'extrato_contaDaniel.pdf')
pdf_info = extract_pdf_info(file_path)

# Integração
if pdf_info:
    print({
        "num_agencia_extrato": pdf_info['agencia'],
        "num_conta_extrato": pdf_info['conta'],
        "data_inicial_extrato": pdf_info['data_inicial'],
        "data_final_extrato": pdf_info['data_final'],
        "saldo_inicial_extrato": pdf_info['saldo_inicial'],
        "saldo_final_extrato": pdf_info['saldo_final'],
    })

# def extract_ofx_info(file_stream):
#     """
#     Extrai informações bancárias de um arquivo OFX.
    
#     Parâmetros:
#     - file_stream: Objeto do arquivo OFX (deve ser aberto no modo leitura ou bytes).
    
#     Retorno:
#     - Um dicionário com as informações extraídas.
#     """
#     try:
#         # Garantir que o arquivo seja seekable, criando um buffer se necessário
#         if isinstance(file_stream, (str, bytes)):
#             file_stream = io.StringIO(file_stream)  # Buffer para texto
#         elif not hasattr(file_stream, "seek"):
#             file_stream = io.StringIO(file_stream.read())  # Transformar em buffer

#         # Fazer o parse do arquivo OFX
#         ofx = ofxparse.OfxParser.parse(file_stream)

#         # Extrair as informações bancárias
#         info = {
#             "cod_banco": int(ofx.account.routing_number),
#             "conta": ofx.account.number,
#             "data_inicial": ofx.account.statement.start_date,
#             "data_final": ofx.account.statement.end_date,
#             "saldo_final": float(ofx.account.statement.balance)
#         }

#         return info

#     except Exception as e:
#         raise ValueError(f"Erro ao processar o arquivo OFX: {str(e)}")

# with open(os.path.join(uplod_folder,"extratoCC.ofx"), "r", encoding="latin-1") as ofx_file:
#     info = extract_ofx_info(ofx_file)
#     print(info)
