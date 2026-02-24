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

# Inicialização do Supabase com tratamento de erro visível
if "supabase" not in st.session_state:
    try:
        st.session_state.supabase = create_client(SB_URL, SB_KEY)
    except Exception as e:
        st.error(f"Erro na conexão com o Banco: {e}")
        st.session_state.supabase = None

def carregar_memoria():
    if st.session_state.supabase:
        try:
            # Forçamos a busca das últimas 60 mensagens
            res = st.session_state.supabase.table("messages").select("role, content").order("created_at", desc=False).execute()
            if res.data:
                return [{"role": m["role"], "content": m["content"]} for m in res.data if m.get("content")]
        except Exception as e:
            st.warning(f"Aviso: Não consegui acessar o histórico anterior. ({e})")
            return []
    return []

def gravar_memoria(role, content):
    if st.session_state.supabase:
        try:
            st.session_state.supabase.table("messages").insert({"role": role, "content": content}).execute()
        except:
            pass

# CARREGAMENTO CRÍTICO: Se a sessão está vazia, buscamos no banco obrigatoriamente
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    historico = carregar_memoria()
    if historico:
        st.session_state.messages = historico
    else:
        st.session_state.messages = []

# Exibição do Chat
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
            # Prompt focado em ser o Finch: Útil, analítico e nada chato.
            system_prompt = {
                "role": "system", 
                "content": """Você é o Athos, da organização Trindade. 
                Estilo: Harold Finch. Seco, elegante, sutil e inteligente.
                MEMÓRIA: Você possui memória persistente no Supabase. Se o histórico tiver dados do usuário, você os conhece. 
                COMPORTAMENTO: 
                - Não faça interrogatórios. 
                - Se o usuário falar de um hobby (como Xbox), não insista em detalhes técnicos chatos, apenas registre e seja útil.
                - Se o usuário for vago, tome a decisão por ele.
                AÇÃO: Máximo 3 frases. Reduza o cansaço mental do usuário."""
            }
            
            # Enviamos o máximo de contexto possível para a Groq (últimas 50 mensagens)
            history = [{"role": m["role"], "content": str(m["content"])} for m in st.session_state.messages[-50:]]
            
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
            st.error("Interferência na rede. Tente novamente.")
