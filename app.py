import streamlit as st
from groq import Groq
from supabase import create_client

# 1. ESTÉTICA, IDENTIDADE E APP (PWA)
LOGO_PATH = "logo.png"
st.set_page_config(page_title="Athos", page_icon=LOGO_PATH, layout="centered")

# CSS para interface limpa e o azul bebê que você escolheu
st.markdown(f"""
    <style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    [data-testid="stImage"] {{ display: flex; justify-content: center; margin: 0 auto; }}
    .main-title {{ text-align: center; font-size: 45px; font-weight: bold; margin-top: -10px; color: white; }}
    .sub-title {{ text-align: center; font-size: 18px; font-style: italic; color: #5dade2; margin-bottom: 30px; }}
    .stDeployButton {{display:none;}}
    </style>
    <link rel="manifest" href="./manifest.json">
    """, unsafe_allow_html=True)

# Cabeçalho Centralizado
col1, col2, col3 = st.columns([1,1,1])
with col2:
    try:
        st.image(LOGO_PATH, width=150)
    except:
        pass

st.markdown('<div class="main-title">Athos</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Vamos conversar?</div>', unsafe_allow_html=True)

# 2. CONEXÕES (Groq + Supabase)
GROQ_KEY = "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"
SB_URL = "https://ovbhqxsseerpjkxmodkv.supabase.co"
SB_KEY = "sb_publishable_Ruf67d-OeRbedGGkHyixHQ_3pW1siBJ"

client = Groq(api_key=GROQ_KEY)

if "supabase" not in st.session_state:
    try:
        st.session_state.supabase = create_client(SB_URL, SB_KEY)
    except:
        st.session_state.supabase = None

# Gestão de Memória Segura
def carregar_memoria():
    if st.session_state.supabase:
        try:
            res = st.session_state.supabase.table("messages").select("*").order("created_at", desc=False).limit(30).execute()
            return [{"role": m["role"], "content": m["content"]} for m in res.data if m.get("content")]
        except:
            return []
    return []

def gravar_memoria(role, content):
    if st.session_state.supabase:
        try:
            st.session_state.supabase.table("messages").insert({"role": role, "content": content}).execute()
        except:
            pass

if "messages" not in st.session_state:
    st.session_state.messages = carregar_memoria()

# Exibição do Chat
for msg in st.session_state.messages:
    avatar = "🕵️‍♂️" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
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
                "content": "Você é o Athos. Personalidade: Harold Finch (sutil, protetor) e Sexta-Feira (analítica). DIRETRIZES: 1. Sem interrogatórios. Interaja organicamente. 2. Memorize dados pessoais e NUNCA repita perguntas. 3. Se o usuário estiver indeciso, tome a decisão por ele (ordem direta e educada). 4. Breve (máx 3 frases), humor sutil, poucos emojis (☕, 🕵️‍♂️). 5. Analise o histórico para não ser repetitivo."
            }
            
            contexto = [system_prompt] + st.session_state.messages[-15:]

            chat_completion = client.chat.completions.create(
                messages=contexto,
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=400
            )
            
            response = chat_completion.choices[0].message.content
            
            if response:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                gravar_memoria("assistant", response)
            else:
                st.error("Tive um pensamento vazio.")

        except Exception:
            st.error("Senti uma interferência técnica. Vamos tentar de novo?")
