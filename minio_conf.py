from minio import Minio
from minio.error import S3Error
import os
import urllib3

# # Configurar conexão HTTPS com certificado confiável
# http_client = urllib3.PoolManager(
#     cert_reqs="CERT_REQUIRED",
#     ca_certs= os.path.dirname(os.path.abspath(__file__)) + "/MINIO/.minio/certs/public.crt"  # Caminho para o certificado
# )
urllib3.disable_warnings()
http_client = urllib3.PoolManager(cert_reqs="CERT_NONE")

MINIO_ENDPOINT = "localhost:9000"  # URL do servidor MinIO
MINIO_ACCESS_KEY = "JPj2A1cPjtwTlrB4JpuN"
MINIO_SECRET_KEY = "1H4VFNxTj3jBqu8Td3apDl80CpkdaCnJN1jxzThA"
MINIO_BUCKET_NAME = "gedcontabilidade"
MINIO_SECURE = True  # Defina como True se o MinIO estiver usando HTTPS

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

