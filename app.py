import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Athos", page_icon="🤖")

# 2. Configuração do "Cérebro" (Sua chave real aqui)
API_KEY = "AIzaSyA60XwLXnK_-qVnV0H5yHUAA6iMizqIxu8"
genai.configure(api_key=API_KEY)

# 3. Definição do Modelo (Usando o 1.5-flash que é o padrão atual)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Interface
st.title("Athos")

# Inicialização do Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibição das mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Lógica de Chat
if prompt := st.chat_input("Diz aí, Batera?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Personalidade Athos (Finch/Sexta-Feira)
            contexto = "Você é o Athos, sutil, inteligente e com humor. Não use scripts de robô. Dê ordens diretas para reduzir o cansaço mental do Moisés."
            
            response = model.generate_content(f"{contexto}\n\nUsuário: {prompt}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erro na conexão: {e}")

# Lembrete de salvamento para o TDAH
st.sidebar.info("Moisés, não esqueça de fazer o Commit no GitHub! 💾")
