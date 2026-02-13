import streamlit as st
import socket

# 1. Configuración de Identidad (Sin que diga Streamlit)
st.set_page_config(
    page_title="Monitoreo Enigma", 
    page_icon="🎼", 
    layout="wide"
)

# 2. Estilo Profesional para el Celular
st.markdown("""
    <style>
    .stSlider { margin-bottom: 10px; }
    h1 { color: #FFD700; text-align: center; text-shadow: 2px 2px #000; font-size: 26px; }
    .stButton>button { background-color: #28a745; color: white; border-radius: 12px; height: 3em; font-weight: bold; }
    .stExpander { background-color: #1e1e1e; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎹 Monitoreo ENIGMA 🎤")

# 3. Buscador y Configuración de Conexión
with st.expander("🔍 CONFIGURACIÓN DE RED (NETBOOK)", expanded=False):
    # Campo para poner la IP que te de la Netbook (ej: 192.168.1.15)
    ip_pc = st.text_input("IP de la Netbook:", value="192.168.1.50", help="Escribí aquí la IP que te dé el comando ipconfig en la PC")
    puerto = 5005
    
    if st.button("PROBAR WI-FI"):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
            s.close()
            st.success(f"Tu Celu está en: {ip_local}")
            st.info(f"Apuntando a Netbook: {ip_pc}")
        except:
            st.error("No hay conexión Wi-Fi activa.")

st.divider()

# 4. Mezcladora de 15 Canales (Cumbia Norteña + Coros)
st.subheader("🎚️ Consola de Mezcla")

instrumentos = [
    "TECLA 1", "TECLA 2", "OCTAPAD 1", "OCTAPAD 2",
    "GUITARRA 1", "GUITARRA 2", "BAJO 1", "BAJO 2",
    "VOZ LÍDER", "ANIMACIÓN", "GÜIRO 1", "GÜIRO 2",
    "CORO 1", "CORO 2", "CORO 3"
]

# Diccionario para guardar los valores actuales
valores_mezcla = {}

# Layout en 3 columnas para que no sea eterno el scroll
cols = st.columns(3)
for i, inst in enumerate(instrumentos):
    with cols[i % 3]:
        # El key es vital para que Streamlit no se confunda
        val = st.slider(inst, 0, 100, 50, key=f"s_{inst}")
        valores_mezcla[inst] = val

st.divider()

# 5. Botón de Envío Real a la PC (APP_STOCK.PY)
if st.button("🚀 ACTUALIZAR MEZCLA EN VIVO", use_container_width=True):
    try:
        # Creamos el socket UDP para enviar datos rápidos
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Enviamos cada canal por separado o en un paquete
        for inst, nivel in valores_mezcla.items():
            mensaje = f"{inst}:{nivel}"
            sock.sendto(mensaje.encode(), (ip_pc, puerto))
        
        st.balloons()
        st.toast(f"¡Mezcla enviada a {ip_pc}!")
    except Exception as e:
        st.error(f"Error al enviar: {e}")
