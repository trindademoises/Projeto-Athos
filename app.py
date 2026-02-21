import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Athos", page_icon="🤖")

# Linha 7: Sua chave real extraída do print
API_KEY = "AIzaSyDeiS0Jzyl6OyrZlyWcr8do54FPO4U8Mnc"
genai.configure(api_key=API_KEY)

# Linha 10: Modelo estável
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Athos")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Diz aí?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Personalidade sutil e direta
            full_prompt = f"Você é o Athos. Responda ao Moisés (Batera): {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erro: {e}")
