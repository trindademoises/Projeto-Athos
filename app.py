import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO DA IDENTIDADE ---
st.set_page_config(
    page_title="Gênesis IA",
    page_icon="logo.png",
    layout="centered"
)

# Truque para esconder a barra do navegador no celular (Modo PWA)
components.html(
    """
    <script>
    const meta = document.createElement('meta');
    meta.name = "apple-mobile-web-app-capable";
    meta.content = "yes";
    window.parent.document.getElementsByTagName('head')[0].appendChild(meta);
    </script>
    """,
    height=0,
)

# --- 2. ESTILO E LOGO ---
st.image("logo.png", width=120)
st.title("Projeto Gênesis")
st.caption("Evolução constante. Decisões precisas.")

# --- 3. LÓGICA DO CHAT (SIMPLIFICADA) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("O que faremos hoje, Batera?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Aqui o Athos assume a personalidade que definimos
        response = "Estou processando sua ordem sob a ótica do Gênesis. Direto e sem rodeios. 🤖🚀" 
        # (Nota: No seu código real, aqui você conecta com a API da Google)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
