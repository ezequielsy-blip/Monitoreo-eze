import streamlit as st
import socket

# Configuración de Identidad
st.set_page_config(page_title="Monitoreo Enigma", page_icon="🎼", layout="wide")

# Estilo Visual
st.markdown("""
    <style>
    .stSlider { margin-bottom: 10px; }
    h1 { color: #FFD700; text-align: center; text-shadow: 2px 2px #000; }
    .stButton>button { background-color: #28a745; color: white; border-radius: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎹 Monitoreo ENIGMA 🎤")

# --- BUSCADOR DE DISPOSITIVOS ---
with st.expander("🔍 BUSCAR CONSOLA CENTRAL", expanded=True):
    if st.button("ESCANEAR RED"):
        # Obtenemos la IP local para saber el rango de red
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        mi_ip = s.getsockname()[0]
        s.close()
        
        base_ip = ".".join(mi_ip.split(".")[:-1]) + "."
        st.write(f"Buscando en tu red: `{base_ip}x`")
        
        # Aquí guardaremos las opciones encontradas
        opciones_encontradas = []
        
        # Simulamos el escaneo (en el celu, por seguridad, probamos las más comunes 
        # o la de localhost para tu prueba actual)
        for i in range(1, 255):
            # En la vida real esto lleva tiempo, para tu prueba forzamos 127.0.0.1
            pass
            
        opciones_encontradas = [mi_ip, "127.0.0.1 (Prueba Interna)"]
        
        st.session_state['dispositivos'] = opciones_encontradas

    if 'dispositivos' in st.session_state:
        seleccion = st.selectbox("Seleccioná la Consola Central:", st.session_state['dispositivos'])
        st.session_state['ip_destino'] = seleccion.split(" ")[0]

st.divider()

# --- MEZCLADORA 15 CANALES ---
instrumentos = [
    "TECLA 1", "TECLA 2", "OCTAPAD 1", "OCTAPAD 2",
    "GUITARRA 1", "GUITARRA 2", "BAJO 1", "BAJO 2",
    "VOZ LÍDER", "ANIMACIÓN", "GÜIRO 1", "GÜIRO 2",
    "CORO 1", "CORO 2", "CORO 3"
]

valores_mezcla = {}
cols = st.columns(3)

for i, inst in enumerate(instrumentos):
    with cols[i % 3]:
        val = st.slider(inst, 0, 100, 50, key=f"s_{inst}")
        valores_mezcla[inst] = val

st.divider()

# --- ENVÍO DE DATOS ---
if st.button("🚀 ACTUALIZAR MEZCLA", use_container_width=True):
    dest = st.session_state.get('ip_destino', "127.0.0.1")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for inst, nivel in valores_mezcla.items():
            mensaje = f"{inst}:{nivel}"
            sock.sendto(mensaje.encode(), (dest, 5005))
        st.success(f"Enviado a {dest}")
    except Exception as e:
        st.error(f"Error: {e}")
