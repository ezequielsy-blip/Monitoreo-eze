import streamlit as st
import socket

# Configuración de la App
st.set_page_config(page_title="Monitoreo Enigma", page_icon="🎼", layout="wide")

# Estilo para que se vea profesional en el celular
st.markdown("""
    <style>
    .stSlider { margin-bottom: 15px; }
    h1 { color: #FFD700; text-align: center; text-shadow: 2px 2px #000; font-size: 24px; }
    .stButton>button { background-color: #28a745; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎹 Monitoreo ENIGMA 🎤")

# --- SECCIÓN DE CONEXIÓN (Buscador) ---
with st.expander("🔍 CONECTAR CON NETBOOK (LOGISTICA)", expanded=False):
    if st.button("ESCANEAR RED WI-FI"):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
            s.close()
            st.success(f"Conectado. Tu IP: {ip_local}")
            st.info("Buscando Netbook para vincular...")
        except:
            st.error("Asegurate de estar en el mismo Wi-Fi que la Netbook.")

st.divider()

# --- MEZCLADORA COMPLETA ---
st.subheader("🎚️ Consola de Mezcla")

instrumentos = [
    "TECLA 1", "TECLA 2", 
    "OCTAPAD 1", "OCTAPAD 2",
    "GUITARRA 1", "GUITARRA 2",
    "BAJO 1", "BAJO 2",
    "VOZ", "ANIMACIÓN",
    "GÜIRO 1", "GÜIRO 2",
    "CORO 1", "CORO 2", "CORO 3"
]

cols = st.columns(3)

for i, inst in enumerate(instrumentos):
    with cols[i % 3]:
        # Usamos el nombre del instrumento como clave única
        st.slider(inst, 0, 100, 50, key=f"slider_{inst}")

st.divider()

if st.button("🚀 ACTUALIZAR MEZCLA EN REAPER", use_container_width=True):
    st.balloons()
    st.toast("Enviando niveles a la Netbook...")
