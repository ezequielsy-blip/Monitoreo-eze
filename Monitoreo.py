import streamlit as st
import socket

st.set_page_config(page_title="Monitoreo ENIGMA", layout="wide")
st.title("🎹 Monitoreo ENIGMA")

# --- BUSCADOR UNIVERSAL POR BROADCAST ---
def busqueda_total():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Permiso para gritar a todos
        s.settimeout(2.0) # Esperamos 2 segundos a que alguien responda
        
        # Gritamos a toda la red en el puerto 5005
        s.sendto("BUSCAR_CONSOLA_ENIGMA".encode(), ('<broadcast>', 5005))
        
        data, addr = s.recvfrom(1024)
        if data.decode() == "AQUI_ESTA_EL_RECEPTOR":
            return addr[0]
    except Exception as e:
        return None
    return None

if st.button("🔍 CONECTAR AUTOMÁTICAMENTE (TODO O NADA)", use_container_width=True):
    ip_encontrada = busqueda_total()
    if ip_encontrada:
        st.session_state['ip_central'] = ip_encontrada
        st.success(f"✅ ¡CONECTADO EXITOSAMENTE A {ip_encontrada}!")
    else:
        st.error("No se encontró nada. Verificá que el Receptor esté en PLAY y en el mismo Wi-Fi.")

st.divider()

# Sliders (15 canales para ENIGMA)
instrumentos = ["TECLA 1", "TECLA 2", "OCTAPAD 1", "OCTAPAD 2", "BAJO 1", "BAJO 2", "GUITARRA 1", "GUITARRA 2", "VOZ LÍDER", "ANIMACIÓN", "GÜIRO 1", "CORO 1", "CORO 2"]
valores = {inst: st.slider(inst, 0, 100, 50, key=inst) for inst in instrumentos}

if st.button("🚀 ACTUALIZAR MEZCLA"):
    ip_destino = st.session_state.get('ip_central')
    if ip_destino:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for inst, nivel in valores.items():
            sock.sendto(f"{inst}:{nivel}".encode(), (ip_destino, 5005))
        st.toast(f"Mezcla enviada a {ip_destino}")
    else:
        st.warning("Primero debés presionar el botón de CONECTAR.")
