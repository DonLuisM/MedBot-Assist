import streamlit as st

st.write('### Hola 🤖. Soy Asistente Virtual MedBot, ¿En qué puedo ayudarte?')

# Inicializar estado de sesión
if 'historial' not in st.session_state:
    st.session_state.historial = []

with st.sidebar:
    st.write('## Configuración MedBot-Assist')
    
    if st.button('Nuevo chat'):
        st.session_state.historial = []
        st.session_state.nuevo_chat = True
        
    if st.session_state.get("nuevo_chat"):
        st.success("✅ Nuevo chat iniciado.")
        st.session_state.nuevo_chat = False


user_input = st.chat_input('Escribe o pega el texto aquí')

if user_input:
    # Mostrar pregunta en un contenedor principal
    with st.container():
        with st.chat_message("user"):
            st.write(user_input)