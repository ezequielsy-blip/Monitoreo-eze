import streamlit as st
import socket

st.title("🎹 Monitoreo ENIGMA")

# Cuadro para poner la IP de tu celular
ip_celu = st.text_input("IP de tu Celular (mirala en el Wi-Fi):", value="0.0.0.0")

instrumentos = ["TECLA 1", "OCTAPAD 2", "BAJO 1", "ANIMACIÓN"]
valores = {inst: st.slider(inst, 0, 100, 50) for inst in instrumentos}

if st.button("🚀 ACTUALIZAR MEZCLA"):
    try:
        # Enviamos a la IP que escribiste arriba
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for inst, nivel in valores.items():
            mensaje = f"{inst}:{nivel}"
            sock.sendto(mensaje.encode(), (ip_celu, 5005))
        st.success(f"Enviado a {ip_celu}")
    except Exception as e:
        st.error(f"Error: {e}")
