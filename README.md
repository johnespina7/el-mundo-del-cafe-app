
# ☕ El Mundo del Café – Recomendador Personalizado

Esta app de Streamlit permite recomendar cafés personalizados según el perfil sensorial y ético de los usuarios. Utiliza inteligencia artificial liviana basada en reglas y análisis de texto para ofrecer recomendaciones precisas a partir de datos obtenidos vía formularios (Tally + Google Sheets) y una base de cafés curada.

---

## 🚀 ¿Qué hace esta app?

- Lee las respuestas del formulario desde Google Sheets.
- Interpreta las preferencias sensoriales y de valor del usuario.
- Compara ese perfil contra una base de datos de cafés extraída de Shopify.
- Muestra 3 cafés recomendados que coinciden con el perfil del usuario.
- Toda la conexión con Google se hace de forma segura usando `st.secrets`.

---

## 🧾 Requisitos

- Cuenta de Google con acceso a:
  - Google Cloud Project con Service Account + API de Sheets activada.
  - Google Sheet con los resultados del formulario de usuario.
- Base de datos `cafes_shopify_export.csv` cargada en el mismo repositorio.
- Archivo `requirements.txt` con las siguientes dependencias:

```txt
streamlit
pandas
gspread
oauth2client
```

---

## 🔐 Configuración de seguridad

1. **NO subas `credentials.json` al repositorio.**
2. Ve a `Settings > Secrets` en Streamlit Cloud.
3. Crea un secreto:

```toml
GOOGLE_CREDENTIALS = '''
{ ... tu archivo credentials.json ... }
'''
```

> Asegúrate de que los saltos de línea estén correctamente escapados (`\n`).

---

## 🛠️ Despliegue en Streamlit Cloud

1. Crea un repositorio GitHub y sube:
   - `app.py` (o `app_streamlit_secure.py`)
   - `requirements.txt`
   - `cafes_shopify_export.csv`
2. Vincula el repositorio en [https://streamlit.io/cloud](https://streamlit.io/cloud).
3. Configura los secretos como se explicó arriba.
4. ¡Listo! Tu recomendador estará en línea para tus usuarios.

---

## ✨ Créditos

Desarrollado por el equipo de El Mundo del Café.  
Una startup que une tecnología, ética y sabor para revolucionar el consumo de café en Latinoamérica.
