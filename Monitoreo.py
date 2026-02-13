import streamlit as st
import socket

st.set_page_config(page_title="Monitoreo ENIGMA", page_icon="🎹")
st.title("🎹 Monitoreo ENIGMA")

# Lista completa de instrumentos
instrumentos = [
    "TECLA 1", "TECLA 2", "OCTAPAD 1", "OCTAPAD 2",
    "GUITARRA 1", "GUITARRA 2", "BAJO 1", "BAJO 2",
    "VOZ", "ANIMACIÓN", "GÜIRO 1", "GÜIRO 2",
    "CORO 1", "CORO 2", "CORO 3"
]

# Definimos los sliders PRIMERO para evitar el NameError
valores_actuales = {}
cols = st.columns(2)
for i, inst in enumerate(instrumentos):
    with cols[i % 2]:
        valores_actuales[inst] = st.slider(inst, 0, 100, 50, key=f"s_{inst}")

st.divider()

# Botón de envío
if st.button("🚀 ACTUALIZAR MEZCLA"):
    try:
        # USAMOS TU IP REAL
        IP_DESTINO = "192.168.3.39" 
        PUERTO = 5005
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Enviamos los datos de los 15 canales
        for inst, nivel in valores_actuales.items():
            mensaje = f"{inst}:{nivel}"
            sock.sendto(mensaje.encode(), (IP_DESTINO, PUERTO))
            
        st.success(f"✅ ¡Mezcla enviada a {IP_DESTINO}!")
    except Exception as e:
        st.error(f"Error: {e}")
