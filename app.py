
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración de página
st.set_page_config(page_title="Tu Café Ideal", layout="centered")
st.title("☕ El Mundo del Café")
st.subheader("Recomendación personalizada de café")

# Autenticación Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
import os
import json

# Leer el secreto como diccionario
creds_json = os.environ["GOOGLE_CREDENTIALS"]
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Leer respuestas desde Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1q0zbnahDvJ9M3WBpLOkqaLkM7VXDfBh8ZW9923MfEg4/edit#gid=0"
worksheet = client.open_by_url(SHEET_URL).sheet1
data = worksheet.get_all_records()
user_df = pd.DataFrame(data)

# Leer último perfil
last_user = user_df.iloc[-1]
user_profile = {
    "gustos": last_user["1. ¿Qué sabores disfrutas más en alimentos o bebidas?(Puedes elegir más de uno)"].lower().split(", "),
    "intensidad": last_user["3. ¿Qué intensidad de sabor prefieres?"].lower(),
    "acidez": last_user["4. ¿Qué nivel de acidez te resulta más agradable?"].lower(),
    "cuerpo": last_user["5. ¿Qué tipo de cuerpo prefieres en un café?"].lower(),
    "valores": last_user["6. ¿Qué atributos valoras más al comprar café?"].lower().split(", ")
}

# Mostrar perfil
st.markdown("### Tu perfil sensorial:")
st.markdown(f"- **Sabores**: {', '.join(user_profile['gustos'])}")
st.markdown(f"- **Intensidad**: {user_profile['intensidad'].capitalize()}")
st.markdown(f"- **Acidez**: {user_profile['acidez'].capitalize()}")
st.markdown(f"- **Cuerpo**: {user_profile['cuerpo'].capitalize()}")
st.markdown(f"- **Valores éticos**: {', '.join(user_profile['valores'])}")

# Leer cafés desde Drive
cafes_df = pd.read_csv("cafes_shopify_export.csv")
cafes_df["Descripción"] = cafes_df["Descripción"].fillna("")
cafes_df["Tags"] = cafes_df["Tags"].fillna("")

# Algoritmo de recomendación
def recomendar_cafe(user, cafes_df):
    def puntuar(fila):
        score = 0
        texto = fila["Descripción"].lower() + " " + fila["Tags"].lower()
        if any(g in texto for g in user["gustos"]):
            score += 1
        if user["intensidad"] in texto:
            score += 1
        if user["acidez"] in texto:
            score += 1
        if user["cuerpo"] in texto:
            score += 1
        if any(v in texto for v in user["valores"]):
            score += 1
        return score

    cafes_df["Puntaje"] = cafes_df.apply(puntuar, axis=1)
    return cafes_df.sort_values("Puntaje", ascending=False).head(3)

# Resultado
st.markdown("### ☕ Recomendación:")
recomendados = recomendar_cafe(user_profile, cafes_df)

for i, row in recomendados.iterrows():
    st.markdown(f"**{row['Nombre del Café']}**")
    st.markdown(f"- {row['Descripción'][:150]}...")
    st.markdown(f"- 💰 Precio: ${row['Precio']}")
    st.markdown("---")
