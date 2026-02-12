import streamlit as st
import socket
import pandas as pd

# Configuración estética
st.set_page_config(page_title="Monitoreo Eze", page_icon="🎼", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stSlider { margin-bottom: 25px; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #1E90FF; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎼 Sistema de Monitoreo - Eze")

# --- BUSCADOR DE DISPOSITIVOS ---
with st.expander("🔍 BUSCAR NETBOOK EN LA RED", expanded=True):
    if st.button("ESCANEAR WI-FI"):
        try:
            # Obtiene la IP base de tu red
            hostname = socket.gethostname()
            ip_propia = socket.gethostbyname(hostname)
            st.write(f"Tu IP: **{ip_propia}**")
            
            # Simulación de detección de la Netbook (esto se conecta con tu script de PC)
            st.success("✅ Netbook 'LOGISTICA' detectada en 192.168.1.50")
        except:
            st.error("No se pudo escanear. Verificá que el Wi-Fi sea el mismo.")

st.divider()

# --- MEZCLADORA DE CANALES ---
st.subheader("🎚️ Mezcla de Monitoreo")
col1, col2 = st.columns(2)

with col1:
    v1 = st.slider("🎤 VOZ PRINCIPAL", 0, 100, 70)
    v2 = st.slider("🎸 GUITARRA", 0, 100, 50)
    v3 = st.slider("🎹 TECLADOS", 0, 100, 40)

with col2:
    v4 = st.slider("🎸 BAJO", 0, 100, 60)
    v5 = st.slider("🥁 BATERÍA", 0, 100, 80)
    v6 = st.slider("📣 COROS", 0, 100, 30)

# --- PANEL DE CONTROL ---
st.divider()
if st.button("🚀 ENVIAR A REAPER"):
    st.balloons()
    st.toast("Mezcla enviada a la Netbook...")
    # Aquí es donde el link de Streamlit mandaría los datos a tu archivo APP_STOCK.PY
