import streamlit as st
import socket

# Configuración de la página
st.set_page_config(page_title="Monitoreo ENIGMA", page_icon="🎼", layout="wide")

st.markdown("<h1>🎹 Monitoreo ENIGMA 🎤</h1>", unsafe_allow_html=True)

# 15 Canales exactos para la banda
instrumentos = [
    "TECLA 1", "TECLA 2", "OCTAPAD 1", "OCTAPAD 2",
    "GUITARRA 1", "GUITARRA 2", "BAJO 1", "BAJO 2",
    "VOZ LÍDER", "ANIMACIÓN", "GÜIRO 1", "GÜIRO 2",
    "CORO 1", "CORO 2", "CORO 3"
]

# Creamos la interfaz
valores_mezcla = {}
cols = st.columns(3)
for i, inst in enumerate(instrumentos):
    with cols[i % 3]:
        valores_mezcla[inst] = st.slider(inst, 0, 100, 50, key=f"s_{inst}")

st.divider()

# Input para la IP de la Netbook (donde está el Reaper)
ip_reaper = st.text_input("IP de la Netbook (Consola Central):", value="127.0.0.1")

if st.button("🚀 ACTUALIZAR MEZCLA EN VIVO", use_container_width=True):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for inst, nivel in valores_mezcla.items():
            mensaje = f"{inst}:{nivel}"
            sock.sendto(mensaje.encode(), (ip_reaper, 5005))
        st.success(f"Enviado a {ip_reaper}")
    except Exception as e:
        st.error(f"Error: {e}")
