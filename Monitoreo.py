if st.button("🚀 ACTUALIZAR MEZCLA"):
    try:
        # IP de prueba interna para el mismo celular
        IP_INTERNA = "127.0.0.1"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        for inst, nivel in valores_mezcla.items():
            mensaje = f"{inst}:{nivel}"
            sock.sendto(mensaje.encode(), (IP_INTERNA, 5005))
        
        st.success("¡Enviado!")
    except Exception as e:
        st.error(f"Error: {e}")
