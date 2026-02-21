import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(page_title="Athos AI", page_icon="🤖", layout="centered")

# --- CONEXÃO COM O CÉREBRO (ATHOS) ---
# Linha 11: Configure sua chave aqui
API_KEY = "AIzaSyA60XwLXnK_-qVnV0H5yHUAA6iMizqIxu8"
genai.configure(api_key=API_KEY)

# Linha 14: Diagnóstico e Definição do Modelo
try:
    # Tenta usar o modelo mais estável disponível
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erro ao carregar o modelo: {e}")

# --- INTERFACE ---
st.image("logo.png", width=80)
st.title("Athos")
st.caption("O braço direito do Moisés")

# Inicializa o histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("Como posso ajudar, Batera?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Comando de personalidade
            full_prompt = f"Você é o Athos, uma IA inteligente, sutil e com humor, inspirada no Finch e na Sexta-Feira. Responda de forma direta ao Moisés (Batera): {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Eita, deu um erro na conexão: {e}")
            st.info("Dica: Se o erro for 404, precisamos verificar se a sua API Key no Google AI Studio está ativa.")

# Salva o que foi feito (Lembrete para o TDAH)
st.sidebar.info("Moisés, não esquece de salvar as alterações no GitHub! 💾")
