from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def upload_imagem_stream(arquivo, nome_original):
    nome_blob = f"{uuid.uuid4()}-{nome_original}"
    blob_client = container_client.get_blob_client(nome_blob)

    blob_client.upload_blob(arquivo, overwrite=True)
    return blob_client.url
