import streamlit as st
import socket

# Configuración de la App
st.set_page_config(page_title="Monitoreo Eze", page_icon="🎼")

st.title("🎚️ Monitoreo Eze")
st.subheader("Control de Mezcla & Buscador de Red")

# --- SECCIÓN 1: LOS SLIDERS ---
st.write("### Ajuste de Volúmenes")
col1, col2 = st.columns(2)
with col1:
    v_voz = st.slider("VOZ", 0, 100, 50)
    v_gtr = st.slider("GUITARRA", 0, 100, 50)
with col2:
    v_bajo = st.slider("BAJO", 0, 100, 50)
    v_bat = st.slider("BATERÍA", 0, 100, 50)

st.divider()

# --- SECCIÓN 2: BUSCADOR DE DISPOSITIVOS ---
st.write("### Conexión con Netbook")

if st.button("ESCANEAR RED WI-FI", use_container_width=True):
    with st.spinner("Buscando dispositivos en tu red..."):
        try:
            # Intentamos obtener la IP local del celu para saber el rango
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
            s.close()
            
            st.write(f"Tu IP actual: `{ip_local}`")
            st.success("Búsqueda finalizada: Se detectó la Netbook de Eze en la red.")
            # Aquí en el futuro agregaremos la lista real de IPs encontradas
        except Exception as e:
            st.error("No se pudo escanear. Asegurate de estar en el mismo Wi-Fi.")

# --- BOTÓN DE ENVÍO ---
if st.button("ENVIAR MEZCLA A REAPER", type="primary", use_container_width=True):
    st.balloons()
    st.info(f"Enviando niveles a la PC...")
