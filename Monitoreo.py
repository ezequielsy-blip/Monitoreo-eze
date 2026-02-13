import streamlit as st
import socket
import concurrent.futures

st.set_page_config(page_title="Monitoreo ENIGMA", layout="wide")
st.title("🎹 Monitoreo ENIGMA")

# --- BUSCADOR QUE ESCANEA TODO ---
def escanear(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.05)
        s.sendto("DAME_IP".encode(), (ip, 5005))
        data, addr = s.recvfrom(1024)
        if data.decode() == "SOY_ENIGMA":
            return ip
    except:
        return None

if st.button("🔍 BUSCAR CONSOLA AUTOMÁTICAMENTE", use_container_width=True):
    # Obtiene la IP de la red local
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    mi_ip = s.getsockname()[0]
    s.close()
    
    prefijo = ".".join(mi_ip.split(".")[:-1]) + "."
    st.info(f"Buscando en red local: {prefijo}x")
    
    # Prueba las 254 IPs al mismo tiempo
    ips = [f"{prefijo}{i}" for i in range(1, 255)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        resultados = list(executor.map(escanear, ips))
    
    final = next((ip for ip in resultados if ip), None)
    if final:
        st.session_state['ip_enigma'] = final
        st.success(f"✅ ¡Consola encontrada en {final}!")
    else:
        st.error("No se encontró nada. ¿Están en el mismo Wi-Fi?")

st.divider()

# Sliders (Sin NameError)
insts = ["TECLA 1", "OCTAPAD 2", "BAJO 1", "VOZ", "COROS"]
vals = {i: st.slider(i, 0, 100, 50, key=i) for i in insts}

if st.button("🚀 ACTUALIZAR"):
    dest = st.session_state.get('ip_enigma')
    if dest:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for k, v in vals.items():
            sock.sendto(f"{k}:{v}".encode(), (dest, 5005))
        st.toast("✅ Enviado")
    else:
        st.warning("Primero buscá la consola.")
