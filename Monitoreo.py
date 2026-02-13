import streamlit as st
import socket
import concurrent.futures

st.set_page_config(page_title="Monitoreo ENIGMA", layout="wide")
st.title("🎹 Monitoreo ENIGMA")

def probar_ip(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.05) # Super rápido para no perder tiempo
        s.sendto("BUSCAR_ENIGMA".encode(), (ip, 5005))
        data, addr = s.recvfrom(1024)
        if data.decode() == "AQUI_ESTOY":
            return ip
    except:
        return None

if st.button("🔍 BUSCAR CONSOLA EN CUALQUIER RED", use_container_width=True):
    try:
        # 1. Detectamos la IP actual del celular (sea la que sea)
        s_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_temp.connect(("8.8.8.8", 80))
        mi_ip = s_temp.getsockname()[0]
        s_temp.close()
        
        # 2. Extraemos el prefijo automáticamente (ej: "192.168.1." o "10.0.0.")
        prefijo = ".".join(mi_ip.split(".")[:-1]) + "."
        st.info(f"Tu red detectada: {prefijo}x. Escaneando...")
        
        # 3. Barremos del 1 al 254 en esa red
        ips_posibles = [f"{prefijo}{i}" for i in range(1, 255)]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            resultados = list(executor.map(probar_ip, ips_posibles))
        
        encontrada = next((ip for ip in resultados if ip), None)
        
        if encontrada:
            st.session_state['ip_enigma'] = encontrada
            st.success(f"✅ ¡Consola encontrada en {encontrada}!")
        else:
            st.error("No se encontró nada. ¿Está el Pydroid en PLAY?")
    except Exception as e:
        st.error(f"Error detectando red: {e}")

st.divider()

# Sliders y envío (igual que antes pero sin errores de NameError)
instrumentos = ["TECLA 1", "OCTAPAD 1", "BAJO 1", "VOZ", "COROS"]
valores = {inst: st.slider(inst, 0, 100, 50, key=inst) for inst in instrumentos}

if st.button("🚀 ACTUALIZAR MEZCLA"):
    ip_dest = st.session_state.get('ip_enigma')
    if ip_dest:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for inst, nivel in valores.items():
            sock.sendto(f"{inst}:{nivel}".encode(), (ip_dest, 5005))
        st.toast(f"Mezcla enviada a {ip_dest}")
    else:
        st.warning("Primero buscá la consola.")
