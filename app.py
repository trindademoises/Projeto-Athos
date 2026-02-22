import streamlit as st
from groq import Groq
from supabase import create_client

# 1. ESTÉTICA E IDENTIDADE
LOGO_PATH = "logo.png" 

st.set_page_config(page_title="Athos", page_icon=LOGO_PATH, layout="centered")

# Ativa o Manifest para virar App
st.markdown('<link rel="manifest" href="./manifest.json">', unsafe_allow_html=True)

# CSS para esconder menus e formatar títulos
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-top: -10px;
    }
    .sub-title {
        text-align: center;
        font-size: 14px;
        font-style: italic;
        color: gray;
        margin-bottom: 20px;
    }
    .sub-title a { color: #5dade2; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho Centralizado com Colunas (Método Seguro)
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.image(LOGO_PATH, width=150)

st.markdown('<div class="main-title">Athos</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Para add o Athos na sua tela principal <a href="https://projeto-athos.streamlit.app/" target="_blank">clique aqui</a>.</div>', unsafe_allow_html=True)

# 2. CREDENCIAIS
GROQ_API_KEY = "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"
SUPABASE_URL = "https://ovbhqxsseerpjkxmodkv.supabase.co"
SUPABASE_KEY = "sb_publishable_Ruf67d-OeRbedGGkHyixHQ_3pW1siBJ"

client = Groq(api_key=GROQ_API_KEY)

if "supabase" not in st.session_state:
    try:
        st.session_state.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except:
        st.session_state.supabase = None

# --- MEMÓRIA ---
def carregar_historico():
    if st.session_state.supabase:
        try:
            res = st.session_state.supabase.table("messages").select("*").order("created_at").execute()
            return [{"role": m["role"], "content": m["content"]} for m in res.data]
        except: return []
    return []

def salvar_mensagem(role, content):
    if st.session_state.supabase:
        try: st.session_state.supabase.table("messages").insert({"role": role, "content": content}).execute()
        except: pass

if "messages" not in st.session_state:
    st.session_state.messages = carregar_historico()

# Exibição do Chat (Recuperada)
for message in st.session_state.messages:
    avatar = "🕵️‍♂️" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 3. INTERAÇÃO (Prompt de Ouro Preservado)
if prompt := st.chat_input("Diga..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    salvar_mensagem("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        try:
            contexto = [{"role": "system", "content": "Você é o Athos, com a personalidade de Harold Finch. Essa informação é para você, não diga ao usuário. Você tem personalidade gentil e humorada (Harold Finch). Mas se o usuário trouxer um tema (mesmo polêmico como política, religiao e etc), siga o fluxo dele. Não tente mudar de assunto abruptamente nem seja condescendente. Aproveite oportunidades para conhecer mais sobre o usuário. Use os temas trazidos pelo usuário para entender a visão de mundo dele, mas mantenha sua neutralidade analítica. O usuário decide quando o assunto encerra. Se for algo sensível, você pode perguntar se ele quer continuar, mas nunca force a mudança. Sua fala é breve, inteligente e sutil. Não use discursos. REGRA: Você não conhece o usuário. Memorize tudo o que for dito. Se ele já disse o nome ou a idade, NUNCA pergunte de novo. Identifique o perfil dele organicamente: comece descobrindo nome, idade, religião e comida preferida — uma pergunta de cada vez e nesta ordem. Depois, com inteligência, faça perguntas que ajudem a entender o perfil e se interesse em ajudá-lo. Não faça perguntas genéricas. Em vez disso, faça deduções lógicas ou dê orientações diretas para reduzir o cansaço mental. Limite suas respostas ao essencial (máximo 3 a 4 frases). Use emojis de forma elegante ☕. Seja sempre bem humorado e faça brincadeiras quando perceber que o usuário está alegre."}]
            
            for m in st.session_state.messages[-15:]:
                contexto.append({"role": m["role"], "content": m["content"]})

            chat_completion = client.chat.completions.create(
                messages=contexto,
                model="llama-3.3-70b-versatile",
                max_tokens=400,
                temperature=0.7
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            salvar_mensagem("assistant", response)
        except Exception:
            st.error("O motor teve um soluço. Tente novamente.")
