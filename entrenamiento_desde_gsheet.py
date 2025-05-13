
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar acceso a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Cargar datos desde la hoja de respuestas
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1q0zbnahDvJ9M3WBpLOkqaLkM7VXDfBh8ZW9923MfEg4/edit#gid=0")
worksheet = spreadsheet.sheet1
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Filtrar columnas relevantes
cols = ["Edad", "Sexo", "Región", "País", "Sabores", "Intensidad", "Acidez", "Cuerpo", "Valores", "Estilo"]
df = df[cols].dropna()

# Convertir categorías a números
encoders = {
    "Sexo": LabelEncoder(),
    "Región": LabelEncoder(),
    "País": LabelEncoder(),
    "Intensidad": LabelEncoder(),
    "Acidez": LabelEncoder(),
    "Cuerpo": LabelEncoder(),
    "Estilo": LabelEncoder()
}
for col, encoder in encoders.items():
    df[col] = encoder.fit_transform(df[col])

# Procesar listas múltiples
df["Sabores"] = df["Sabores"].str.lower().str.split(", ")
df["Valores"] = df["Valores"].str.lower().str.split(", ")

mlb_sabores = MultiLabelBinarizer()
mlb_valores = MultiLabelBinarizer()
sabores_encoded = pd.DataFrame(mlb_sabores.fit_transform(df["Sabores"]), columns=mlb_sabores.classes_)
valores_encoded = pd.DataFrame(mlb_valores.fit_transform(df["Valores"]), columns=mlb_valores.classes_)

df_final = pd.concat([
    df.drop(columns=["Sabores", "Valores"]),
    sabores_encoded,
    valores_encoded
], axis=1)

# Clustering
kmeans = KMeans(n_clusters=4, random_state=42)
df_final["Cluster"] = kmeans.fit_predict(df_final)

# Visualización
pca = PCA(n_components=2)
components = pca.fit_transform(df_final.drop(columns=["Cluster"]))
df_final["PCA1"] = components[:, 0]
df_final["PCA2"] = components[:, 1]

plt.figure(figsize=(10,6))
sns.scatterplot(data=df_final, x="PCA1", y="PCA2", hue="Cluster", palette="viridis")
plt.title("Clustering de perfiles sensoriales y demográficos")
plt.savefig("clustering_perfiles.png")
plt.show()

# Guardar resultados
df_final.to_csv("clusters_perfiles.csv", index=False)
