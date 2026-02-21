import streamlit as st
import google.generativeai as genai

# Configuração básica
st.set_page_config(page_title="Athos AI", page_icon="🤖")

# Linha 7: Conexão direta com sua chave nova
genai.configure(api_key="AIzaSyDeiS0Jzyl6OyrZlyWcr8do54FPO4...", transport='rest')

# Linha 10: Definição do modelo
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Athos")
st.caption("O braço direito do Moisés")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Diz aí, Batera?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Personalidade Athos
            full_prompt = f"Você é o Athos, IA inspirada em Finch e Sexta-Feira. Responda ao Moisés (Batera): {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erro: {e}")

st.sidebar.info("Moisés, salvou no GitHub? 💾")
