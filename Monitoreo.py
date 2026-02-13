import streamlit as st
import socket

st.title("🎹 Monitoreo ENIGMA")

# Función de conexión forzada
def conectar_ya():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.settimeout(1.5)
        # Grito universal
        s.sendto("BUSCAR_CONSOLA_ENIGMA".encode(), ('<broadcast>', 5005))
        data, addr = s.recvfrom(1024)
        return addr[0]
    except:
        return None

if st.button("🔍 CONECTAR AHORA"):
    ip = conectar_ya()
    if ip:
        st.session_state['ip'] = ip
        st.success(f"✅ ¡ENCONTRADO EN {ip}!")
    else:
        st.error("No se encuentra. REVISÁ QUE EL WI-FI ESTÉ PRENDIDO.")

# Sliders definidos ANTES de usarlos para evitar el NameError
insts = ["TECLA 1", "TECLA 2", "OCTAPAD 1", "BAJO 1", "VOZ"]
vals = {i: st.slider(i, 0, 100, 50, key=i) for i in insts}

if st.button("🚀 ENVIAR"):
    ip_dest = st.session_state.get('ip')
    if ip_dest:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for k, v in vals.items():
            sock.sendto(f"{k}:{v}".encode(), (ip_dest, 5005))
        st.toast("Enviado")
