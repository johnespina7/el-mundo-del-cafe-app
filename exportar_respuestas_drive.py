
import gspread
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials
import os

# Configuración de autenticación
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Abrir el spreadsheet
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1q0zbnahDvJ9M3WBpLOkqaLkM7VXDfBh8ZW9923MfEg4/edit#gid=0"
spreadsheet = client.open_by_url(spreadsheet_url)
worksheet = spreadsheet.sheet1

# Obtener datos como DataFrame
records = worksheet.get_all_records()
df = pd.DataFrame(records)

# Verificar o crear carpeta destino
folder_path = "algoritmo_cafe"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Guardar CSV
csv_path = os.path.join(folder_path, "respuestas_formulario_export.csv")
df.to_csv(csv_path, index=False)
print(f"✅ Archivo exportado correctamente a: {csv_path}")
