import streamlit as st
from langchain_ollama import ChatOllama
import time

st.write('### Hola 🤖. Soy tú Asistente Virtual MedBot, ¿En qué puedo ayudarte?')

# Inicializar estado de sesión
if 'historial' not in st.session_state:
    st.session_state.historial = []
        
with st.sidebar:
    st.write('## Configuración MedBot-Assist')
    
    left, right = st.columns(2)
    if left.button('Nuevo chat', icon="🗒️", use_container_width=True):
        st.session_state.historial = []
        st.session_state.nuevo_chat = True
        
    if st.session_state.get("nuevo_chat"):
        st.toast("✅ Nuevo chat iniciado.")
        st.session_state.nuevo_chat = False
    

    with right.popover("Config.", icon="⚙️"):
        st.session_state.temperature = st.slider(
            'Temperatura',
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.1
        )
        st.session_state.top_p = st.slider(
            'Top P',
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            step=0.1
        )
        st.session_state.top_k = st.slider(
            'Top K',
            min_value=0,
            max_value=100,
            value=50,
            step=1
        )
        st.session_state.max_tokens = st.slider(
            'Max Tokens',
            min_value=1,
            max_value=4096,
            value=256,
            step=1
        )
            

model_name = "qwen3"
user_input = st.chat_input('Escribe o pega el texto aquí')

if user_input:
    # Mostrar pregunta en un contenedor principal
    with st.container():
        with st.chat_message("user"):
            st.write(user_input)
                    
    llm = ChatOllama(
        model=model_name,
        temperature=st.session_state.temperature,
        top_p=st.session_state.top_p,
        top_k=st.session_state.top_k,
        num_predict=st.session_state.max_tokens
    )
  
    prompt = "You are a medical assistant that helps doctors to agilice procedures. /nothink"
    messages = [
        ("system", prompt),
        ("human", user_input)
    ]
  
    # Generar y mostrar respuesta
    with st.spinner(f"*Pensando con {model_name}...*"):
        response = llm.invoke(messages)

        st.write("**Respuesta:**")
        st.write(response.content)
        
        # Metadata de la respuesta
        st.caption(f"""
        **Detalles Técnicos:**
        - Tokens usados: {response.response_metadata['eval_count']}
        - Tiempo respuesta: {response.response_metadata['total_duration'] / 1e9:.2f}s
        - Modelo preciso: {response.response_metadata['model']}
        """)
        
        # Guardar en historial
        st.session_state.historial.append({
            "modelo": model_name,
            "pregunta": user_input,
            "respuesta": response.content,
            "metadata": response.response_metadata
        })