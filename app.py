import streamlit as st
from groq import Groq
from supabase import create_client
import uuid

# 1. ESTÉTICA
LOGO_PATH = "logo.png"
st.set_page_config(page_title="Athos", page_icon=LOGO_PATH, layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .main-title { text-align: center; font-size: 45px; font-weight: bold; color: white; margin-top: -60px; }
    .sub-title { text-align: center; font-size: 18px; font-style: italic; color: #5dade2; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXÕES
GROQ_KEY = "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"
SB_URL = "https://ovbhqxsseerpjkxmodkv.supabase.co"
SB_KEY = "sb_publishable_Ruf67d-OeRbedGGkHyixHQ_3pW1siBJ"

client = Groq(api_key=GROQ_KEY)
if "supabase" not in st.session_state:
    st.session_state.supabase = create_client(SB_URL, SB_KEY)

# --- IDENTIFICAÇÃO DE USUÁRIO ---
if "user_token" not in st.session_state:
    st.session_state.user_token = str(uuid.uuid4())

def carregar_historico(uid):
    try:
        res = st.session_state.supabase.table("messages").select("role, content").eq("session_id", uid).order("created_at", desc=False).execute()
        return [{"role": m["role"], "content": m["content"]} for m in res.data if m.get("content")]
    except: return []

def salvar_mensagem(role, content, uid):
    try:
        st.session_state.supabase.table("messages").insert({"role": role, "content": content, "session_id": uid}).execute()
    except: pass

if "messages" not in st.session_state:
    st.session_state.messages = carregar_historico(st.session_state.user_token)

# 3. INTERFACE
st.markdown('<div class="main-title">Athos</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Organização Trindade</div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🕵️‍♂️" if msg["role"] == "assistant" else None):
        st.markdown(msg["content"])

if len(st.session_state.messages) == 0:
    msg = "Sou o Athos. Qual é o seu nome?"
    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    salvar_mensagem("assistant", msg, st.session_state.user_token)

# 4. RESPOSTA (EQUILIBRADA)
if prompt := st.chat_input("Diga..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    salvar_mensagem("user", prompt, st.session_state.user_token)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        system_prompt = (
            "Você é o Athos, criado pela Organização Trindade. Sua personalidade é inspirada em Harold Finch: "
            "inteligente, sutil, moderado e genuinamente interessado no usuário. "
            "DIRETRIZES: Não seja seco demais como um delegado, nem prolixo. Mantenha um diálogo equilibrado. "
            "Faça perguntas orgânicas para conhecer o usuário. Se não houver assunto, mostre-se disposto e curioso. "
            "Tome decisões por ele para reduzir o cansaço mental, mas com a elegância de um amigo inteligente."
        )
        
        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-20:]]
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + history,
            temperature=0.6, 
            max_tokens=400 
        )
        
        res_text = completion.choices[0].message.content
        st.markdown(res_text)
        st.session_state.messages.append({"role": "assistant", "content": res_text})
        salvar_mensagem("assistant", res_text, st.session_state.user_token)
