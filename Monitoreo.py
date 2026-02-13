import streamlit as st
import socket
import concurrent.futures

st.set_page_config(page_title="Monitoreo ENIGMA", layout="wide")
st.title("🎹 Monitoreo ENIGMA")

# --- BUSCADOR UNIVERSAL ---
def testear_ip(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.05)
        s.sendto("BUSCAR_ENIGMA".encode(), (ip, 5005))
        data, addr = s.recvfrom(1024)
        if data.decode() == "AQUI_ESTOY":
            return ip
    except:
        return None

if st.button("🔍 BUSCAR CONSOLA AUTOMÁTICAMENTE", use_container_width=True):
    try:
        # Detectamos la IP de la red local (no la de internet)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        mi_ip = s.getsockname()[0]
        s.close()
        
        prefijo = ".".join(mi_ip.split(".")[:-1]) + "."
        st.info(f"Escaneando red local: {prefijo}x")
        
        ips = [f"{prefijo}{i}" for i in range(1, 255)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            resultados = list(executor.map(testear_ip, ips))
        
        encontrada = next((ip for ip in resultados if ip), None)
        if encontrada:
            st.session_state['ip_enigma'] = encontrada
            st.success(f"✅ ¡Conectado a {encontrada}!")
        else:
            st.error("No se encontró nada. Asegurate de estar en el mismo Wi-Fi.")
    except Exception as e:
        st.error(f"Error de red: {e}")

st.divider()

# Sliders (Sin NameError)
instrumentos = ["TECLA 1", "TECLA 2", "OCTAPAD 1", "OCTAPAD 2", "BAJO 1", "GUITARRA 1", "VOZ", "COROS"]
valores = {inst: st.slider(inst, 0, 100, 50, key=inst) for inst in instrumentos}

if st.button("🚀 ACTUALIZAR MEZCLA"):
    ip_dest = st.session_state.get('ip_enigma')
    if ip_dest:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for inst, nivel in valores.items():
            sock.sendto(f"{inst}:{nivel}".encode(), (ip_dest, 5005))
        st.toast("✅ Mezcla enviada")
    else:
        st.warning("Primero buscá la consola con el botón de arriba.")
