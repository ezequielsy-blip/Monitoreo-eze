import streamlit as st
import socket

st.set_page_config(page_title="Selector ENIGMA", page_icon="🎧")
st.title("🎧 Selector de Monitoreo ENIGMA")

# Lista de canales disponibles en el Reaper
canales = {
    "CANAL 1: TECLAS": 1,
    "CANAL 2: OCTAPAD": 2,
    "CANAL 3: BAJO": 3,
    "CANAL 4: GUITARRA": 4,
    "CANAL 5: VOZ LÍDER": 5,
    "CANAL 6: COROS": 6
}

st.subheader("Seleccioná tu mezcla personal:")
seleccion = st.selectbox("¿Quién sos hoy?", list(canales.keys()))

if st.button("🔊 CONECTAR MI MONITOREO", use_container_width=True):
    try:
        # Aquí la app le avisa a la Netbook qué canal rutear por el cable virtual
        canal_id = canales[seleccion]
        
        # IP de la Netbook (Asumiendo que estás en su Hotspot o Wi-Fi)
        IP_NETBOOK = "192.168.43.1" 
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(f"SET_MONITOR_CHANNEL:{canal_id}".encode(), (IP_NETBOOK, 5005))
        
        st.success(f"✅ Escuchando {seleccion}. ¡Ponete los auriculares!")
        st.info("Recordá tener AudioRelay abierto para recibir el sonido.")
    except Exception as e:
        st.error("Error: Asegurate de estar en el Wi-Fi de la banda.")
