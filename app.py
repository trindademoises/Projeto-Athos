import streamlit as st
from groq import Groq
from supabase import create_client

# 1. CONFIGURAÇÃO DE IDENTIDADE E APP
LOGO_PATH = "logo.png"
st.set_page_config(page_title="Athos", page_icon=LOGO_PATH, layout="centered")

# Injeção de CSS para centralização e estética (O azul bebê que você gostou)
st.markdown(f"""
    <style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    [data-testid="stImage"] {{ display: flex; justify-content: center; margin: 0 auto; }}
    .main-title {{ text-align: center; font-size: 45px; font-weight: bold; margin-top: -10px; color: white; }}
    .sub-title {{ text-align: center; font-size: 18px; font-style: italic; color: #5dade2; margin-bottom: 30px; }}
    </style>
    <link rel="manifest" href="./manifest.json">
    """, unsafe_allow_html=True)

# Cabeçalho
col1, col2, col3 = st.columns([1,1,1])
with col2:
    try: st.image(LOGO_PATH, width=150)
    except: pass

st.markdown('<div class="main-title">Athos</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Vamos conversar?</div>', unsafe_allow_html=True)

# 2. CONEXÕES EXTERNAS (Groq + Supabase)
GROQ_KEY = "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"
SB_URL = "https://ovbhqxsseerpjkxmodkv.supabase.co"
SB_KEY = "sb_publishable_Ruf67d-OeRbedGGkHyixHQ_3pW1siBJ"

client = Groq(api_key=GROQ_KEY)

if "supabase" not in st.session_state:
    try: st.session_state.supabase = create_client(SB_URL, SB_KEY)
    except: st.session_state.supabase = None

# Gestão de Memória
def carregar_memoria():
    if st.session_state.supabase:
        try:
            res = st.session_state.supabase.table("messages").select("*").order("created_at", desc=False).limit(30).execute()
            return [{"role": m["role"], "content": m["content"]} for m in res.data]
        except: return []
    return []

def gravar_memoria(role, content):
    if st.session_state.supabase:
        try: st.session_state.supabase.table("messages").insert({"role": role, "content": content}).execute()
        except: pass

if "messages" not in st.session_state:
    st.session_state.messages = carregar_memoria()

# Exibição das mensagens
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🕵️‍♂️" if msg["role"]=="assistant" else None):
        st.markdown(msg["content"])

# 3. O CÉREBRO DO ATHOS (Instrução "Vá Além")
if prompt := st.chat_input("Diga..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    gravar_memoria("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        try:
            # PROMPT SYSTEM REESTRUTURADO (Personalidade Pura)
            system_prompt = {
                "role": "system",
                "content": """Você é o Athos. Sua personalidade é uma fusão de Harold Finch (sutil, protetor, inteligente) e Sexta-Feira (eficiente, analítico). 
                DIRETRIZES:
                1. NÃO faça interrogatórios. Não siga listas de perguntas.
                2. Seja um observador. Aprenda sobre o usuário através do fluxo natural da conversa.
                3. Se o usuário te contar algo (nome, preferência, TDAH, time), guarde isso para sempre e NUNCA pergunte de novo.
                4. Reduza o cansaço mental do usuário: tome decisões por ele quando solicitado. Se ele estiver indeciso, dê UMA ordem direta com educação.
                5. Estilo de fala: Breve, elegante, com humor sutil e poucos emojis (☕, 🕵️‍♂️, 🎯).
                6. Se o usuário estiver desmotivado, seja o suporte dele, não um robô chato. 
                7. Analise o contexto das últimas mensagens antes de responder para nunca ser repetitivo."""
            }
            
            # Construção do contexto (Sistema + Últimas 20 mensagens)
            contexto = [system_prompt] + st.session_state.messages[-20:]

            response = client.chat.completions.create(
                messages=contexto,
                model="llama-3.3-70b-versatile",
                temperature=0.6, # Menos aleatório, mais preciso
                max_tokens=500
            ).choices[0].message.content

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            gravar_memoria("assistant", response)
        except:
            st.error("Desculpe, tive um breve lapso. Pode repetir?")
