
import streamlit as st
import pandas as pd

# ----------------------------
# Configuración y título
# ----------------------------
st.set_page_config(page_title="Recomendador de Café", layout="centered")
st.title("☕ El Mundo del Café")
st.subheader("Descubre tu café ideal según tus gustos")

# ----------------------------
# Formulario interactivo
# ----------------------------
with st.form("formulario_cafe"):
    nombre = st.text_input("¿Cuál es tu nombre?")
    correo = st.text_input("¿Cuál es tu correo electrónico?")
    
    sabores = st.multiselect(
        "1. ¿Qué sabores disfrutas más en alimentos o bebidas?",
        ["Frutas dulces", "Nueces", "Especias (canela, clavo, etc.)", "Frutas cítricas",
         "Chocolate", "Miel o caramelo", "Hierbas o flores", "Sabores amargos o intensos"]
    )

    intensidad = st.radio(
        "2. ¿Qué intensidad de sabor prefieres?",
        ["Suave", "Equilibrado", "Intenso"]
    )

    acidez = st.radio(
        "3. ¿Qué nivel de acidez te resulta más agradable?",
        ["Baja", "Media", "Alta"]
    )

    cuerpo = st.radio(
        "4. ¿Qué tipo de cuerpo prefieres en un café?",
        ["Ligero", "Medio", "Denso"]
    )

    valores = st.multiselect(
        "5. ¿Qué atributos valoras más al comprar café?",
        ["Comercio justo", "Prácticas agrícolas sostenibles o regenerativas", "Origen nacional o latinoamericano"]
    )

    enviado = st.form_submit_button("Descubrir mi café ideal")

# ----------------------------
# Algoritmo de recomendación
# ----------------------------
if enviado:
    st.markdown("### 👤 Tu perfil sensorial:")
    st.markdown(f"- **Nombre**: {nombre}")
    st.markdown(f"- **Sabores**: {', '.join(sabores)}")
    st.markdown(f"- **Intensidad**: {intensidad}")
    st.markdown(f"- **Acidez**: {acidez}")
    st.markdown(f"- **Cuerpo**: {cuerpo}")
    st.markdown(f"- **Valores éticos**: {', '.join(valores)}")

    user_profile = {
        "gustos": [s.lower() for s in sabores],
        "intensidad": intensidad.lower(),
        "acidez": acidez.lower(),
        "cuerpo": cuerpo.lower(),
        "valores": [v.lower() for v in valores]
    }

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

    st.markdown("### ☕ Tu recomendación:")
    recomendados = recomendar_cafe(user_profile, cafes_df)

    for i, row in recomendados.iterrows():
        st.markdown(f"**{row['Nombre del Café']}**")
        st.markdown(f"- {row['Descripción'][:150]}...")
        st.markdown(f"- 💰 Precio: ${row['Precio']}")
        st.markdown("---")
