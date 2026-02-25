import streamlit as st
from groq import Groq
from supabase import create_client
import extra_streamlit_components as stx
import uuid

# 1. CONFIGURAÇÃO E ESTÉTICA (ESTILO FINCH/SEXTA-FEIRA)
LOGO_PATH = "logo.png"
st.set_page_config(page_title="Athos", page_icon=LOGO_PATH, layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .main-title { text-align: center; font-size: 45px; font-weight: bold; color: white; margin-top: -60px; }
    .sub-title { text-align: center; font-size: 18px; font-style: italic; color: #5dade2; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CREDENCIAIS (SUPABASE E GROQ)
GROQ_KEY = "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"
SB_URL = "https://ovbhqxsseerpjkxmodkv.supabase.co"
SB_KEY = "sb_publishable_Ruf67d-OeRbedGGkHyixHQ_3pW1siBJ"

client = Groq(api_key=GROQ_KEY)
if "supabase" not in st.session_state:
    st.session_state.supabase = create_client(SB_URL, SB_KEY)

# --- GERENCIADOR DE IDENTIDADE (COOKIES) ---
cookie_manager = stx.CookieManager()
user_token = cookie_manager.get("athos_user_token")

# Se o navegador não tiver um token, criamos um agora
if not user_token:
    user_token = str(uuid.uuid4())
    cookie_manager.set("athos_user_token", user_token, key="set_user_token")

# --- FUNÇÕES DE MEMÓRIA ---
def carregar_historico(uid):
    try:
        res = st.session_state.supabase.table("messages").select("role, content").eq("session_id", uid).order("created_at", desc=False).execute()
        return [{"role": m["role"], "content": m["content"]} for m in res.data if m.get("content")]
    except: return []

def salvar_mensagem(role, content, uid):
    try:
        st.session_state.supabase.table("messages").insert({"role": role, "content": content, "session_id": uid}).execute()
    except: pass

# Inicializa o estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = carregar_historico(user_token)
    st.session_state.first_run = True

# 3. INTERFACE DO CHAT
st.markdown('<div class="main-title">Athos</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Criado pela Organização Trindade</div>', unsafe_allow_html=True)

# Exibe mensagens anteriores
for msg in st.session_state.messages:
    avatar = "🕵️‍♂️" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- LÓGICA DE BOAS-VINDAS PERSONALIZADA ---
if len(st.session_state.messages) == 0:
    # Cenário 1: Novo Utilizador
    welcome_text = "Olá, eu sou o Athos. Qual é o seu nome?"
    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        st.markdown(welcome_text)
    st.session_state.messages.append({"role": "assistant", "content": welcome_text})
    salvar_mensagem("assistant", welcome_text, user_token)

elif st.session_state.first_run:
    # Cenário 2: Utilizador já conhecido (Voltando)
    try:
        # O Athos analisa o histórico para saudar pelo nome organicamente
        contexto = st.session_state.messages[-15:]
        saudacao_ia = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é o Athos. O usuário está voltando. Analise o histórico e saúde-o pelo nome de forma elegante e sutil. Pergunte no que pode ajudar hoje. Seja breve."},
                {"role": "user", "content": "Olá, entrei na aplicação agora."}
            ] + contexto
        )
        msg_volta = saudacao_ia.choices[0].message.content
        with st.chat_message("assistant", avatar="🕵️‍♂️"):
            st.markdown(msg_volta)
        st.session_state.messages.append({"role": "assistant", "content": msg_volta})
        salvar_mensagem("assistant", msg_volta, user_token)
        st.session_state.first_run = False # Impede de repetir a saudação em cada refresh
    except:
        st.session_state.first_run = False

# 4. ENTRADA DE DADOS E RESPOSTA
if prompt := st.chat_input("Como posso ajudar?"):
    # Mostra e salva a pergunta do utilizador
    st.session_state.messages.append({"role": "user", "content": prompt})
    salvar_mensagem("user", prompt, user_token)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta do Athos
    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        system_prompt = (
            "Você é o Athos, criado pela organização Trindade. "
            "Sua personalidade combina Harold Finch e Sexta-Feira (Iron Man). "
            "Seja inteligente, sutil, tenha humor e reduza o cansaço mental do usuário. "
            "Não dê opções, dê orientações diretas baseadas no perfil que identificar."
        )
        
        full_history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-20:]]
        
        response_ia = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + full_history,
            temperature=0.6
        )
        
        texto_resposta = response_ia.choices[0].message.content
        st.markdown(texto_resposta)
        
        st.session_state.messages.append({"role": "assistant", "content": texto_resposta})
        salvar_mensagem("assistant", texto_resposta, user_token)
