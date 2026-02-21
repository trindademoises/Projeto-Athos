import streamlit as st
import google.generativeai as genai

# Configuração da página (Voltando ao original)
st.set_page_config(page_title="Athos", page_icon="🤖")

# Linha 7: Voltando para a chave que você já tinha e que não dava erro 400
# RECOLE AQUI A SUA CHAVE QUE COMEÇA COM AIza...
genai.configure(api_key="COLE_AQUI_A_SUA_CHAVE_ANTIGA")

# Linha 10: Modelo estável
model = genai.GenerativeModel('gemini-pro')

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
            # Voltando ao prompt original
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erro: {e}")
