from minio import Minio
from minio.error import S3Error
import os
import urllib3
from env.credenciais import ENDPOINT, ACCESS_KEY, SECRET_KEY,BUCKET_NAME,SECURE

# # Configurar conexão HTTPS com certificado confiável
# http_client = urllib3.PoolManager(
#     cert_reqs="CERT_REQUIRED",
#     ca_certs= os.path.dirname(os.path.abspath(__file__)) + "/MINIO/.minio/certs/public.crt"  # Caminho para o certificado
# )
urllib3.disable_warnings()
http_client = urllib3.PoolManager(cert_reqs="CERT_NONE")

MINIO_ENDPOINT = ENDPOINT  # URL do servidor MinIO
MINIO_ACCESS_KEY = ACCESS_KEY
MINIO_SECRET_KEY = SECRET_KEY
MINIO_BUCKET_NAME = BUCKET_NAME
MINIO_SECURE = SECURE  # Defina como True se o MinIO estiver usando HTTPS

# Inicializa o cliente MinIO
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE,
    http_client=http_client
)

# Verifica se o bucket existe, caso contrário, cria-o
def create_minio_bucket():
    if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
        minio_client.make_bucket(MINIO_BUCKET_NAME)

