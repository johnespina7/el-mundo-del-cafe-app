
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import datetime

# ----------------------------
# CONFIGURACIÓN INICIAL
# ----------------------------
st.set_page_config(page_title="Descubre tu Café Ideal", layout="centered")
st.title("☕ El Mundo del Café")
st.subheader("Responde este breve formulario y descubre tu café ideal")

# ----------------------------
# AUTENTICACIÓN A GOOGLE SHEETS
# ----------------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1q0zbnahDvJ9M3WBpLOkqaLkM7VXDfBh8ZW9923MfEg4/edit#gid=0")
worksheet = sheet.sheet1

# ----------------------------
# FORMULARIO
# ----------------------------
with st.form("formulario_completo"):
    st.markdown("### 1. ¿Qué sabores disfrutas más en alimentos o bebidas?")
    sabores = st.multiselect("", ["Chocolate", "Frutas cítricas", "Frutas dulces", "Nueces", "Especias (canela, clavo, etc.)", "Miel o caramelo", "Hierbas o flores", "Sabores amargos o intensos"])

    st.markdown("### 2. ¿Qué tipo de aroma te atrae más en un café?")
    aroma = st.radio("", ["Dulce y achocolatado", "Floral y frutal", "Especiado o herbal", "Tostado o ahumado", "No lo sé / me da igual"])

    st.markdown("### 3. ¿Qué intensidad de sabor prefieres?")
    intensidad = st.radio("", ["Suave y delicado", "Equilibrado", "Intenso y robusto"])

    st.markdown("### 4. ¿Qué nivel de acidez te resulta más agradable?")
    acidez = st.radio("", ["Baja", "Media", "Alta", "No lo sé / no tengo preferencia"])

    st.markdown("### 5. ¿Qué tipo de cuerpo prefieres en un café?")
    cuerpo = st.radio("", ["Ligero", "Medio", "Denso / Cremoso", "No lo sé / no tengo claro"])

    st.markdown("### 6. ¿Qué atributos valoras más al comprar café?")
    valores = st.multiselect("", ["Comercio justo / precio justo al productor", "Prácticas agrícolas sostenibles o regenerativas", "Producción artesanal", "Origen nacional o latinoamericano", "Variedad sensorial / innovación"])

    st.markdown("### 7. ¿Con qué frecuencia tomas café?")
    frecuencia = st.radio("", ["1 vez al día o menos", "2 a 3 veces al día", "Más de 3 veces al día"])

    st.markdown("### 8. ¿Cómo preparas tu café habitualmente?")
    preparacion = st.multiselect("", ["Espresso", "Prensa francesa", "V60 o filtrado manual", "Cafetera italiana / moka", "Cold Brew", "Cafetera automática", "No sé / quiero explorar"])

    st.markdown("### 9. ¿Qué tan aventurero eres con nuevos sabores?")
    aventura = st.radio("", ["Me gusta experimentar", "Prefiero ir a la segura", "Me da lo mismo"])

    st.markdown("### 10. ¿Te gustan cafés suaves o con carácter?")
    estilo = st.radio("", ["Suaves", "Balanceados", "Con carácter"])

    st.markdown("### 11. Tu nombre y correo electrónico")
    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo")

    enviado = st.form_submit_button("Obtener mi recomendación")

# ----------------------------
# PROCESAR RESPUESTAS + RECOMENDACIÓN
# ----------------------------
if enviado:
    respuestas = [
        datetime.datetime.now().isoformat(),
        nombre,
        correo,
        ", ".join(sabores),
        aroma,
        intensidad,
        acidez,
        cuerpo,
        ", ".join(valores),
        frecuencia,
        ", ".join(preparacion),
        aventura,
        estilo
    ]
    worksheet.append_row(respuestas)

    st.success("¡Gracias por completar tu perfil! ☕ Aquí tienes tu recomendación personalizada.")
    st.markdown("---")

    # PERFIL DEL USUARIO
    user_profile = {
        "gustos": [s.lower() for s in sabores],
        "intensidad": intensidad.lower(),
        "acidez": acidez.lower(),
        "cuerpo": cuerpo.lower(),
        "valores": [v.lower() for v in valores]
    }

    # CARGAR BASE DE DATOS DE CAFÉS
    cafes_df = pd.read_csv("cafes_shopify_export.csv")
    cafes_df["Descripción"] = cafes_df["Descripción"].fillna("")
    cafes_df["Tags"] = cafes_df["Tags"].fillna("")

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
        return cafes_df.sort_values("Puntaje", ascending=False).drop_duplicates("Nombre del Café").head(3)

    st.markdown("### ☕ Recomendación personalizada:")

    recomendados = recomendar_cafe(user_profile, cafes_df)

    for i, row in recomendados.iterrows():
        st.markdown(f"**{row['Nombre del Café']}**")
        st.markdown(f"- {row['Descripción'][:150]}...")
        st.markdown(f"- 💰 Precio: ${row['Precio']}")
        st.markdown("---")
