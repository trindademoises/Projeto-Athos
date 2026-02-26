import streamlit as st
from groq import Groq
from supabase import create_client
import uuid

# 1. ESTÉTICA (MANTIDA)
LOGO_PATH = "logo.png"
st.set_page_config(page_title="Athos", page_icon=LOGO_PATH, layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .main-title { text-align: center; font-size: 45px; font-weight: bold; color: white; margin-top: -60px; }
    .sub-title { text-align: center; font-size: 18px; font-style: italic; color: #5dade2; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXÕES (MANTIDAS)
GROQ_KEY = "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"
SB_URL = "https://ovbhqxsseerpjkxmodkv.supabase.co"
SB_KEY = "sb_publishable_Ruf67d-OeRbedGGkHyixHQ_3pW1siBJ"

client = Groq(api_key=GROQ_KEY)
if "supabase" not in st.session_state:
    st.session_state.supabase = create_client(SB_URL, SB_KEY)

# --- CORREÇÃO DA MEMÓRIA (USANDO PARÂMETRO NA URL PARA PERSISTÊNCIA) ---
# Se não houver um ID na URL, ele cria um e fixa. Isso garante que ele te reconheça.
if "u" not in st.query_params:
    st.query_params["u"] = str(uuid.uuid4())[:8]
user_token = st.query_params["u"]

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
    st.session_state.messages = carregar_historico(user_token)

# 3. INTERFACE (MANTIDA)
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
    salvar_mensagem("assistant", msg, user_token)

# 4. RESPOSTA (TRAVA DE 1 PERGUNTA E PERSONALIDADE FINCH)
if prompt := st.chat_input("Diga..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    salvar_mensagem("user", prompt, user_token)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        system_prompt = (
            "Você é o Athos, da Organização Trindade. Persona: Harold Finch. "
            "Sutil, inteligente e observador. "
            "REGRA CRÍTICA: Faça APENAS UMA pergunta por resposta. Nunca duas ou mais. "
            "Se o usuário mencionar um interesse, comente brevemente e faça sua única pergunta. "
            "Responda em no máximo 3 frases."
        )
        
        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-15:]]
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + history,
            temperature=0.2, # Baixado para 0.2 para ele obedecer cegamente as regras
            max_tokens=200 
        )
        
        res_text = completion.choices[0].message.content
        st.markdown(res_text)
        st.session_state.messages.append({"role": "assistant", "content": res_text})
        salvar_mensagem("assistant", res_text, user_token)
