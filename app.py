import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO DA IDENTIDADE ---
st.set_page_config(
    page_title="Athos IA",
    page_icon="logo.png",
    layout="centered"
)

# Configura a Inteligência do Athos
genai.configure(api_key="AIzaSyA60XwLXnK_-qVnV0H5yHUAA6iMizqIxu8")
model = genai.GenerativeModel('gemini-pro')
# Truque para transformar em App no Celular
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

# --- VISUAL DO TOPO ---
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=80)
with col2:
    st.markdown("### OLÁ! 😁")
    st.markdown("**Sou o Athos!** Sua IA de decisões precisas e evolução constante.")

st.divider()

# --- LÓGICA DO CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("O que faremos hoje, Batera?"):
    # Adiciona a pergunta do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta do Athos
    with st.chat_message("assistant"):
        # Instrução oculta para manter a personalidade que você gosta
        contexto = (
            "Você é o Athos, uma IA decisiva. Personalidade: Finch/Sexta-Feira. "
            "Usuário: Moisés (Batera). Seja direto, decida por ele, use 1-2 emojis. "
            "Se for a primeira interação, pergunte o nome se não souber."
        )
        
        try:
            # Chama o Google Gemini
            response = model.generate_content(f"{contexto} \n\n Pergunta: {prompt}")
            texto_resposta = response.text
            st.markdown(texto_resposta)
            st.session_state.messages.append({"role": "assistant", "content": texto_resposta})
        except Exception as e:
            st.error(f"Eita, deu um erro na conexão: {e}")

