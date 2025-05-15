import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Clusters de Café", layout="wide")

st.title("📊 Análisis de Perfiles de Café")
st.markdown("Visualización de usuarios segmentados por gustos, atributos y características sensoriales.")

# Cargar dataset procesado
try:
    df = pd.read_csv("algoritmo_cafe/modelos/dataset_entrenado.csv")
    st.success(f"✅ Datos cargados: {df.shape[0]} registros")
except FileNotFoundError:
    st.error("❌ No se encontró el archivo dataset_entrenado.csv. Asegúrate de ejecutar el entrenamiento.")
    st.stop()

# Visualización de distribución de clusters
st.subheader("Distribución de Clusters")
fig, ax = plt.subplots()
sns.countplot(x="cluster", data=df, palette="muted", ax=ax)
ax.set_title("Cantidad de usuarios por grupo")
ax.set_xlabel("Cluster")
ax.set_ylabel("Usuarios")
st.pyplot(fig)

# Visualización por dimensión
st.subheader("Análisis por Dimensión")

dimensiones = [col for col in df.columns if col != "cluster"]

dimension = st.selectbox("Selecciona una dimensión", opciones := sorted(dimensiones))

fig2, ax2 = plt.subplots()
sns.boxplot(x="cluster", y=dimension, data=df, palette="Set2", ax=ax2)
ax2.set_title(f"Distribución de '{dimension}' por Cluster")
st.pyplot(fig2)

# Mostrar tabla por cluster
st.subheader("🔎 Ver Datos por Cluster")
selected_cluster = st.selectbox("Selecciona un cluster para ver sus características", sorted(df["cluster"].unique()))
filtered = df[df["cluster"] == selected_cluster]
st.dataframe(filtered.head(20))