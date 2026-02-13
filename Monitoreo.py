import streamlit as st
import socket
import concurrent.futures

st.set_page_config(page_title="Monitoreo ENIGMA", page_icon="🎹", layout="wide")
st.title("🎹 Monitoreo ENIGMA")

# --- LÓGICA DEL BUSCADOR AUTOMÁTICO ---
def intentar_conectar(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1) # Tiempo ultra corto para escaneo rápido
        s.sendto("BUSCAR_CONSOLA_ENIGMA".encode(), (ip, 5005))
        data, addr = s.recvfrom(1024)
        if data.decode() == "AQUI_ESTA_EL_RECEPTOR":
            return ip
    except:
        return None

def escanear_red():
    # 1. Obtener mi propia IP para saber el rango
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    mi_ip = s.getsockname()[0]
    s.close()
    
    base_ip = ".".join(mi_ip.split(".")[:-1]) + "."
    lista_ips = [f"{base_ip}{i}" for i in range(1, 255)]
    
    # 2. Escaneo multihilo (Prueba todas las IPs a la vez)
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        resultados = list(executor.map(intentar_conectar, lista_ips))
    
    return next((ip for ip in resultados if ip is not None), None)

# --- INTERFAZ ---
if st.button("🔍 BUSCAR CONSOLA EN LA RED", use_container_width=True):
    con_ip = escanear_red()
    if con_ip:
        st.session_state['ip_central'] = con_ip
        st.success(f"✅ ¡Conectado a la Consola en: {con_ip}!")
    else:
        st.error("No se encontró ningún receptor activo en esta red.")

st.divider()

# --- MEZCLA (15 CANALES) ---
instrumentos = [
    "TECLA 1", "TECLA 2", "OCTAPAD 1", "OCTAPAD 2",
    "GUITARRA 1", "GUITARRA 2", "BAJO 1", "BAJO 2",
    "VOZ LÍDER", "ANIMACIÓN", "GÜIRO 1", "GÜIRO 2",
    "CORO 1", "CORO 2", "CORO 3"
]

valores = {}
cols = st.columns(3)
for i, inst in enumerate(instrumentos):
    with cols[i % 3]:
        valores[inst] = st.slider(inst, 0, 100, 50, key=inst)

if st.button("🚀 ACTUALIZAR MEZCLA"):
    ip_destino = st.session_state.get('ip_central')
    if ip_destino:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for inst, nivel in valores.items():
            sock.sendto(f"{inst}:{nivel}".encode(), (ip_destino, 5005))
        st.toast(f"Enviado a {ip_destino}")
    else:
        st.warning("Primero debes buscar la consola central.")
