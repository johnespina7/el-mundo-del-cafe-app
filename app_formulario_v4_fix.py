
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import datetime
import hashlib

# CONFIGURACIÓN
st.set_page_config(page_title="Descubre tu Café Ideal", layout="centered")
st.title("☕ El Mundo del Café")
st.subheader("Descubre el café ideal para ti, según tus gustos, valores y perfil demográfico")

# AUTENTICACIÓN GOOGLE SHEETS
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1q0zbnahDvJ9M3WBpLOkqaLkM7VXDfBh8ZW9923MfEg4/edit#gid=0")
worksheet = sheet.sheet1

# VALIDAR ENCABEZADOS (sin resize)
expected_headers = ['Timestamp', 'Nombre', 'Correo', 'Edad', 'Sexo', 'Comuna', 'Región', 'País', 'Sabores', 'Aroma', 'Intensidad', 'Acidez', 'Cuerpo', 'Valores', 'Frecuencia', 'Preparación', 'Aventura', 'Estilo', 'Hash Perfil', 'Cafés recomendados']
existing_headers = worksheet.row_values(1)
if existing_headers != expected_headers:
    worksheet.insert_row(expected_headers, 1)

# HISTORIAL
try:
    historial_df = pd.DataFrame(worksheet.get_all_records())
except:
    historial_df = pd.DataFrame()

# FORMULARIO
with st.form("formulario"):
    nombre = st.text_input("Tu nombre")
    correo = st.text_input("Tu correo electrónico")
    edad = st.number_input("Edad", min_value=10, max_value=100, step=1)
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro", "Prefiero no decirlo"])
    comuna = st.text_input("Comuna")
    region = st.text_input("Región")
    pais = st.text_input("País")

    sabores = st.multiselect("¿Qué sabores disfrutas más?", [
        "Chocolate", "Frutas cítricas", "Frutas dulces", "Nueces", "Especias (canela, clavo, etc.)",
        "Miel o caramelo", "Hierbas o flores", "Sabores amargos o intensos"])

    aroma = st.radio("¿Qué tipo de aroma te atrae más en un café?", [
        "Dulce y achocolatado", "Floral y frutal", "Especiado o herbal", "Tostado o ahumado", "No lo sé / me da igual"])

    intensidad = st.radio("¿Qué intensidad de sabor prefieres?", [
        "Suave y delicado", "Equilibrado", "Intenso y robusto"])

    acidez = st.radio("¿Qué nivel de acidez prefieres?", [
        "Baja", "Media", "Alta", "No lo sé / no tengo preferencia"])

    cuerpo = st.radio("¿Qué tipo de cuerpo prefieres en un café?", [
        "Ligero", "Medio", "Denso / Cremoso", "No lo sé / no tengo claro"])

    valores = st.multiselect("¿Qué atributos valoras más al comprar café?", [
        "Comercio justo / precio justo al productor", "Prácticas agrícolas sostenibles o regenerativas",
        "Producción artesanal", "Origen nacional o latinoamericano", "Variedad sensorial / innovación"])

    frecuencia = st.radio("¿Con qué frecuencia tomas café?", [
        "1 vez al día o menos", "2 a 3 veces al día", "Más de 3 veces al día"])

    preparacion = st.multiselect("¿Cómo preparas tu café habitualmente?", [
        "Espresso", "Prensa francesa", "V60 o filtrado manual", "Cafetera italiana / moka",
        "Cold Brew", "Cafetera automática", "No sé / quiero explorar"])

    aventura = st.radio("¿Qué tan aventurero eres con nuevos sabores?", [
        "Me gusta experimentar", "Prefiero ir a la segura", "Me da lo mismo"])

    estilo = st.radio("¿Te gustan cafés suaves o con carácter?", [
        "Suaves", "Balanceados", "Con carácter"])

    enviado = st.form_submit_button("Obtener recomendación")

# PROCESAMIENTO
if enviado:
    campos = [nombre, correo, edad, sexo, comuna, region, pais, sabores, aroma, intensidad, acidez,
              cuerpo, valores, frecuencia, preparacion, aventura, estilo]
    if any(c == "" or c == [] for c in campos):
        st.error("Por favor completa todas las respuestas.")
    else:
        perfil_raw = f"{sabores}-{aroma}-{intensidad}-{acidez}-{cuerpo}-{valores}-{frecuencia}-{preparacion}-{aventura}-{estilo}"
        hash_perfil = hashlib.sha256(perfil_raw.encode()).hexdigest()

        mismo_usuario = historial_df[historial_df["Correo"] == correo]
        if not mismo_usuario.empty and hash_perfil in mismo_usuario["Hash Perfil"].values:
            st.success("Tu perfil no ha cambiado. Mostrando tu recomendación anterior.")
            recomendacion_anterior = mismo_usuario[mismo_usuario["Hash Perfil"] == hash_perfil]["Cafés recomendados"].values[0]
            st.markdown(f"**☕ Cafés recomendados anteriormente:** {recomendacion_anterior}")
        else:
            nueva_respuesta = [
                datetime.datetime.now().isoformat(), nombre, correo, edad, sexo, comuna, region, pais,
                ", ".join(sabores), aroma, intensidad, acidez, cuerpo,
                ", ".join(valores), frecuencia, ", ".join(preparacion),
                aventura, estilo, hash_perfil, ""
            ]
            worksheet.append_row(nueva_respuesta)
            st.success("✅ Recomendación enviada y almacenada (simulada).")
