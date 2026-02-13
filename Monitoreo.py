import streamlit as st
import socket

st.set_page_config(page_title="Monitoreo Enigma", page_icon="🎼")

st.title("🎹 Monitoreo ENIGMA")

# 15 Canales de Enigma
instrumentos = [
    "TECLA 1", "TECLA 2", "OCTAPAD 1", "OCTAPAD 2",
    "GUITARRA 1", "GUITARRA 2", "BAJO 1", "BAJO 2",
    "VOZ LÍDER", "ANIMACIÓN", "GÜIRO 1", "GÜIRO 2",
    "CORO 1", "CORO 2", "CORO 3"
]

# Creamos los sliders
valores = {}
cols = st.columns(3)
for i, inst in enumerate(instrumentos):
    with cols[i % 3]:
        valores[inst] = st.slider(inst, 0, 100, 50, key=inst)

st.divider()

# Botón de envío forzado a prueba interna
if st.button("🚀 ACTUALIZAR MEZCLA"):
    try:
        # 127.0.0.1 es la IP para que el celu se hable a sí mismo
        IP_INTERNA = "127.0.0.1"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        for inst, nivel in valores.items():
            mensaje = f"{inst}:{nivel}"
            sock.sendto(mensaje.encode(), (IP_INTERNA, 5005))
            
        st.success("¡Datos enviados al servidor interno!")
    except Exception as e:
        st.error(f"Error de envío: {e}")
