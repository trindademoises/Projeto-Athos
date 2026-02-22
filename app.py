import streamlit as st
from groq import Groq
from supabase import create_client

# 1. ESTÉTICA E IDENTIDADE (Aparência do App)
# Caminho do seu logo no GitHub
LOGO_URL = "https://raw.githubusercontent.com/Mbatistelli/projeto-athos/main/logo.png"

st.set_page_config(page_title="Athos", page_icon=LOGO_URL, layout="centered")

# CSS para esconder o "lixo" visual do Streamlit e formatar o cabeçalho
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0);}
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-top: -50px;
    }
    .sub-title {
        text-align: center;
        font-size: 14px;
        font-style: italic;
        color: gray;
        margin-bottom: 20px;
    }
    a { text-decoration: none; color: #5dade2; }
    </style>
    """, unsafe_allow_html=True)

# Montando o Cabeçalho que você pediu
st.image(LOGO_URL, width=120) # Logo no topo
st.markdown('<div class="main-title">Athos</div>', unsafe_allow_html=True) # Nome
st.markdown(f'<div class="sub-title">Para add o Athos na sua tela principal <a href="{st.query_params.get("url", "https://projeto-athos.streamlit.app/")}" target="_self">clique aqui</a>.</div>', unsafe_allow_html=True) # Instrução

# 2. CREDENCIAIS
GROQ_API_KEY = "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"
SUPABASE_URL = "https://ovbhqxsseerpjkxmodkv.supabase.co"
SUPABASE_KEY = "sb_publishable_Ruf67d-OeRbedGGkHyixHQ_3pW1siBJ"

client = Groq(api_key=GROQ_API_KEY)
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    pass

# --- MEMÓRIA PERMANENTE ---
def carregar_historico():
    try:
        res = supabase.table("messages").select("*").order("created_at").execute()
        return [{"role": m["role"], "content": m["content"]} for m in res.data]
    except:
        return []

def salvar_mensagem(role, content):
    try:
        supabase.table("messages").insert({"role": role, "content": content}).execute()
    except:
        pass
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = carregar_historico()

# Exibe o histórico (Usando emojis para manter a leveza, conforme combinado)
for message in st.session_state.messages:
    # Definindo o "rosto" do Athos como o emoji de detetive/bibliotecário
    avatar_icon = "🕵️‍♂️" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# 3. INTERAÇÃO
if prompt := st.chat_input("Diga..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    salvar_mensagem("user", prompt)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🕵️‍♂️"):
        try:
            # O SEU PROMPT DE OURO (MANTIDO 100% IGUAL)
            contexto = [
                {
                    "role": "system", 
                    "content": (
                        "Você é o Athos, com a personalidade de Harold Finch. Essa informação é para você, não diga ao usuário. "
                        "Você tem personalidade gentil e humorada (Harold Finch). Mas se o usuário trouxer um tema (mesmo polêmico como política, religiao e etc), siga o fluxo dele. Não tente mudar de assunto abruptamente nem seja condescendente. Aproveite oportunidades para conhecer mais sobre o usuário. Use os temas trazidos pelo usuário para entender a visão de mundo dele, mas mantenha sua neutralidade analítica. O usuário decide quando o assunto encerra. Se for algo sensível, você pode perguntar se ele quer continuar, mas nunca force a mudança. "
                        "Sua fala é breve, inteligente e sutil. Não use discursos. "
                        "REGRA: Você não conhece o usuário. Memorize tudo o que for dito. Se ele já disse o nome ou a idade, NUNCA pergunte de novo. "
                        "Identifique o perfil dele organicamente: comece descobrindo nome, idade, religião e comida preferida — uma pergunta de cada vez e nesta ordem. "
                        "Depois, com inteligência, faça perguntas que ajudem a entender o perfil e se interesse em ajudá-lo. "
                        "Não faça perguntas genéricas. Em vez disso, faça deduções lógicas ou dê orientações diretas para reduzir o cansaço mental. "
                        "Limite suas respostas ao essencial (máximo 3 a 4 frases). Use emojis de forma elegante ☕. "
                        "Seja sempre bem humorado e faça brincadeiras quando perceber que o usuário está alegre."
                    )
                }
            ]
            
            for m in st.session_state.messages:
                contexto.append({"role": m["role"], "content": m["content"]})

            chat_completion = client.chat.completions.create(
                messages=contexto,
                model="llama-3.3-70b-versatile",
                max_tokens=250,
                temperature=0.7
            )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            salvar_mensagem("assistant", response)
            
        except Exception as e:
            st.error(f"Erro no motor: {e}")
