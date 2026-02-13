import streamlit as st
import socket
import concurrent.futures

st.set_page_config(page_title="Mi Mezcla ENIGMA")
st.title("🎧 Mi Monitoreo ENIGMA")

# --- BUSCADOR DE PC (Evita confusión con otros celus) ---
def buscar_pc(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)
        s.sendto("QUIEN_ES_LA_PC".encode(), (ip, 5005))
        data, addr = s.recvfrom(1024)
        if data.decode() == "SOY_LA_PC_CENTRAL":
            return ip
    except:
        return None

if st.button("🔍 ENCONTRAR CONSOLA CENTRAL", use_container_width=True):
    with st.spinner("Buscando a la PC en la red..."):
        # Detecta IP local ignorando el 4G
        s_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s_temp.connect(("8.8.8.8", 80))
        base_ip = ".".join(s_temp.getsockname()[0].split(".")[:-1]) + "."
        s_temp.close()
        
        ips = [f"{base_ip}{i}" for i in range(1, 255)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            resultados = list(executor.map(buscar_pc, ips))
        
        pc_ip = next((ip for ip in resultados if ip), None)
        if pc_ip:
            st.session_state['pc_ip'] = pc_ip
            st.success(f"✅ Conectado a la PC: {pc_ip}")
        else:
            st.error("❌ No se encontró la PC. Revisá el Wi-Fi.")

st.divider()

# --- CONTROL DEL MÚSICO ---
if 'pc_ip' in st.session_state:
    canal = st.selectbox("Elegí tu número de mezcla:", [f"Canal {i}" for i in range(1, 11)])
    vol_master = st.slider("Volumen Maestro de tus Auriculares", 0, 100, 80)
    
    if st.button("🔊 APLICAR VOLUMEN"):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = f"VOL_MASTER:{canal}:{vol_master}"
        sock.sendto(msg.encode(), (st.session_state['pc_ip'], 5005))
        st.toast(f"Volumen de {canal} actualizado")
else:
    st.info("💡 Presioná 'ENCONTRAR CONSOLA' para empezar.")
