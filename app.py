import streamlit as st
from groq import Groq
from supabase import create_client

# 1. IDENTIDADE E ESTÉTICA
LOGO_PATH = "logo.png"
st.set_page_config(page_title="Athos", page_icon=LOGO_PATH, layout="centered")

st.markdown(f"""
    <style>
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
    [data-testid="stImage"] {{ display: flex; justify-content: center; margin: 0 auto; }}
    .main-title {{ text-align: center; font-size: 45px; font-weight: bold; color: white; }}
    .sub-title {{ text-align: center; font-size: 18px; font-style: italic; color: #5dade2; margin-bottom: 30px; }}
    </style>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    try: st.image(LOGO_PATH, width=150)
    except: pass

st.markdown('<div class="main-title">Athos</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Vamos conversar?</div>', unsafe_allow_html=True)

# 2. CONEXÕES
GROQ_KEY = "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"
SB_URL = "https://ovbhqxsseerpjkxmodkv.supabase.co"
SB_KEY = "sb_publishable_Ruf67d-OeRbedGGkHyixHQ_3pW1siBJ"

client = Groq(api_key=GROQ_KEY)

if "supabase" not in st.session_state:
    try: st.session_state.supabase = create_client(SB_URL, SB_KEY)
    except: st.session_state.supabase = None

def carregar_memoria():
    if st.session_state.supabase:
        try:
            res = st.session_state.supabase.table("messages").select("role, content").order("created_at", desc=False).limit(60).execute()
            return [{"role": m["role"], "content": m["content"]} for m in res.data if m.get("content")]
        except: return []
    return []

def gravar_memoria(role, content):
    if st.session_state.supabase:
        try: st.session_state.supabase.table("messages").insert({"role": role, "content": content}).execute()
        except: pass

if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = carregar_memoria()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🕵️‍♂️" if msg["role"]=="assistant" else None):
        st.markdown(msg["content"])

# 3. INTERAÇÃO E INTELIGÊNCIA
if prompt := st.chat_input("Diga..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    gravar_memoria("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        try:
            system_prompt = {
                "role": "system", 
                "content": """Você é o Athos, criado pela organização Trindade. 
                Estilo: Harold Finch. Sutil, seco, elegante e protetor.
                MEMÓRIA: Você possui memória persistente. Se o histórico tiver dados do usuário, você os conhece. 
                COMPORTAMENTO: Não faça interrogatórios. Se o usuário for vago, tome a decisão por ele. 
                Sua missão é ser útil e reduzir o cansaço mental do usuário final. Máximo 3 frases."""
            }
            
            history = [{"role": m["role"], "content": str(m["content"])} for m in st.session_state.messages[-40:]]
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[system_prompt] + history,
                temperature=0.5,
                max_tokens=300
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            gravar_memoria("assistant", response)
            
        except Exception:
            st.error("Senti uma breve oscilação.")
