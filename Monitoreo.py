import streamlit as st
import socket

st.title("🎹 Monitoreo ENIGMA (Canal Directo)")

# Sliders (Sin errores de definición)
insts = ["TECLA 1", "OCTAPAD", "BAJO", "VOZ LÍDER"]
valores = {i: st.slider(i, 0, 100, 50, key=i) for i in insts}

if st.button("🚀 TRANSMITIR A LA BANDA", use_container_width=True):
    try:
        MCAST_GRP = '224.1.1.1'
        MCAST_PORT = 5007
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        
        for k, v in valores.items():
            msg = f"{k}:{v}"
            sock.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
            
        st.success("✅ Transmisión enviada al aire.")
    except Exception as e:
        st.error(f"Error de antena: {e}")
