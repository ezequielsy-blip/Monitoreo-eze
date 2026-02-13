import streamlit as st
import socket

st.set_page_config(page_title="Monitoreo ENIGMA", page_icon="🎹")

st.title("🎹 Monitoreo ENIGMA")

# Definimos los instrumentos
instrumentos = [
    "TECLA 1", "OCTAPAD 2", "BAJO 1", "ANIMACIÓN",
    "TECLA 2", "OCTAPAD 1", "GUITARRA 1", "GUITARRA 2",
    "BAJO 2", "VOZ", "GÜIRO 1", "GÜIRO 2",
    "CORO 1", "CORO 2", "CORO 3"
]

# Creamos los sliders y guardamos sus valores en un diccionario
# Esto evita el NameError
valores_actuales = {}
cols = st.columns(2)

for i, inst in enumerate(instrumentos):
    with cols[i % 2]:
        valores_actuales[inst] = st.slider(inst, 0, 100, 50, key=f"s_{inst}")

st.divider()

# Botón de envío
if st.button("🚀 ACTUALIZAR MEZCLA"):
    try:
        # IP de prueba interna para el mismo celular
        IP_INTERNA = "127.0.0.1"
        PUERTO = 5005
        
        # Creamos el socket dentro del botón
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        for inst, nivel in valores_actuales.items():
            mensaje = f"{inst}:{nivel}"
            sock.sendto(mensaje.encode(), (IP_INTERNA, PUERTO))
        
        st.success("¡Enviado al servidor de prueba!")
    except Exception as e:
        st.error(f"Error al enviar: {e}")
