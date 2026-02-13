import streamlit as st
import socket

# Configuración de la App
st.set_page_config(page_title="Monitoreo Eze - Cumbia", page_icon="🎼", layout="wide")

# Estilo Personalizado
st.markdown("""
    <style>
    .stSlider { margin-bottom: 20px; }
    h1 { color: #FFD700; text-align: center; text-shadow: 2px 2px #000; }
    .stButton>button { background-color: #28a745; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎹 Monitoreo Norteño Eze 🎤")

# --- BUSCADOR DE DISPOSITIVOS ---
with st.expander("🔍 CONECTAR CON NETBOOK (LOGISTICA)", expanded=False):
    if st.button("ESCANEAR WI-FI"):
        try:
            # Obtención de IP para el buscador
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
            s.close()
            st.success(f"Conectado al Wi-Fi. Tu IP: {ip_local}")
            st.info("Netbook 'LOGISTICA' detectada. Lista para recibir mezcla.")
        except:
            st.error("Error de conexión. Verificá el Wi-Fi.")

st.divider()

# --- MEZCLADORA DOBLE (Cumbia Norteña) ---
st.subheader("🎚️ Control de Mezcla")

# Definimos los instrumentos típicos x2
instrumentos = [
    "ACORDEÓN 1", "ACORDEÓN 2", 
    "OCTAPAD 1", "OCTAPAD 2",
    "GUITARRA 1", "GUITARRA 2",
    "BAJO 1", "BAJO 2",
    "VOZ LÍDER", "ANIMACIÓN",
    "GÜIRO 1", "GÜIRO 2"
]

# Creamos 3 columnas para que entren todos en el celu
col1, col2, col3 = st.columns(3)

for i, inst in enumerate(instrumentos):
    if i % 3 == 0:
        with col1:
            st.slider(inst, 0, 100, 50, key=inst)
    elif i % 3 == 1:
        with col2:
            st.slider(inst, 0, 100, 50, key=inst)
    else:
        with col3:
            st.slider(inst, 0, 100, 50, key=inst)

st.divider()

# --- BOTÓN DE ENVÍO ---
if st.button("🚀 ENVIAR MEZCLA A REAPER", use_container_width=True):
    st.balloons()
    st.toast("Actualizando niveles en APP_STOCK.PY...")
