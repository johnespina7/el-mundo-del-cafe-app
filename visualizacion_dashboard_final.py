import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os
import glob

st.set_page_config(page_title="Dashboard de Perfiles de Café", layout="wide")

st.title("📊 Análisis de Perfiles de Café")
st.markdown("Visualización de usuarios segmentados por gustos, atributos y características sensoriales.")

# Buscar archivo dataset más reciente en la carpeta raíz del proyecto
folder_path = "algoritmo_cafe/"
pattern = os.path.join(folder_path, "dataset_entrenado_*.csv")
files = glob.glob(pattern)

if not files:
    st.error("❌ No se encontró ningún archivo 'dataset_entrenado_*.csv'. Ejecuta primero el entrenamiento.")
    st.stop()

# Seleccionar el archivo más reciente
latest_file = max(files, key=os.path.getctime)
st.success(f"✅ Dataset cargado: `{os.path.basename(latest_file)}`")

# Cargar dataset
df = pd.read_csv(latest_file)

# Mostrar total de registros
st.markdown(f"### 👥 Total de perfiles: {len(df)}")

# Columnas de análisis
gustos_col = "1. ¿Qué sabores disfrutas más en alimentos o bebidas?(Puedes elegir más de uno)"
intensidad_col = "3. ¿Qué intensidad de sabor prefieres?"
acidez_col = "4. ¿Qué nivel de acidez te resulta más agradable?"
cuerpo_col = "5. ¿Qué tipo de cuerpo prefieres en un café?"
valores_col = "6. ¿Qué atributos valoras más al comprar café?"

# Columnas en 3
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### ☕ Intensidad")
    st.bar_chart(df[intensidad_col].value_counts())

with col2:
    st.markdown("### 🍋 Acidez")
    st.bar_chart(df[acidez_col].value_counts())

with col3:
    st.markdown("### 🧈 Cuerpo")
    st.bar_chart(df[cuerpo_col].value_counts())

# Gráfico de Sabores Favoritos
st.markdown("### 🌈 Sabores Favoritos")
gustos = df[gustos_col].dropna().apply(lambda x: [g.strip().lower() for g in x.split(',')])
todos_los_gustos = Counter([g for sublist in gustos for g in sublist])
gustos_df = pd.DataFrame.from_dict(todos_los_gustos, orient='index', columns=['Frecuencia'])
gustos_df = gustos_df.sort_values(by="Frecuencia", ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=gustos_df.index, y=gustos_df['Frecuencia'], palette="viridis", ax=ax)
plt.xticks(rotation=45)
plt.title("Frecuencia de sabores preferidos")
st.pyplot(fig)

# Gráfico de valores éticos
st.markdown("### 🌱 Valores Éticos al Comprar Café")
valores = df[valores_col].dropna().apply(lambda x: [v.strip().lower() for v in x.split(',')])
todos_los_valores = Counter([v for sublist in valores for v in sublist])
valores_df = pd.DataFrame.from_dict(todos_los_valores, orient='index', columns=['Frecuencia'])
valores_df = valores_df.sort_values(by="Frecuencia", ascending=True)

fig2, ax2 = plt.subplots(figsize=(8, 4))
valores_df.plot(kind="barh", legend=False, ax=ax2, color="darkgreen")
plt.title("Atributos más valorados por los usuarios")
st.pyplot(fig2)

# Tabla de datos crudos
with st.expander("📄 Ver tabla completa de respuestas"):
    st.dataframe(df)