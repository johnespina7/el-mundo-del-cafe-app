import os
import mimetypes
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Configuración
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Autenticación
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# Verificar o crear carpeta "algoritmo_cafe"
folder_name = "algoritmo_cafe"
folder_id = None

# Buscar si existe
results = drive_service.files().list(
    q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
    spaces='drive',
    fields='files(id, name)',
).execute()
items = results.get('files', [])

if items:
    folder_id = items[0]['id']
else:
    # Crear carpeta si no existe
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    folder_id = folder.get('id')

# Archivos a subir
files_to_upload = [
    "algoritmo_cafe/modelos/modelo_kmeans.pkl",
    "algoritmo_cafe/modelos/dataset_entrenado.csv"
]

for file_path in files_to_upload:
    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        mime_type = mimetypes.guess_type(file_path)[0]
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, mimetype=mime_type)
        uploaded = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"✅ Archivo subido: {file_name}")
    else:
        print(f"⚠️ Archivo no encontrado: {file_path}")