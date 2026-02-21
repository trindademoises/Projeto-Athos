import streamlit as st
from groq import Groq
from supabase import create_client

# 1. Configuração da Página
st.set_page_config(page_title="Athos", page_icon="🤖")

# 2. Credenciais
GROQ_API_KEY = "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"
SUPABASE_URL = "https://ovbhqxsseerpjkxmodkv.supabase.co"
SUPABASE_KEY = "sb_publishable_Ruf67d-OeRbedGGkHyixHQ_3pW1siBJ"

client = Groq(api_key=GROQ_API_KEY)
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    pass

st.title("Athos")

# Inicialização do Histórico na Sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Interação
if prompt := st.chat_input("Diga..."):
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # CONSTRUÇÃO DA MEMÓRIA: Sistema + Histórico Completo
            contexto = [
                {
                    "role": "system", 
                    "content": (
                        "Você é o Athos, com a personalidade de Harold Finch. Essa informação é para você, não diga ao usuário. "
                        "Sua fala é breve, inteligente e sutil. Não use discursos. "
                        "REGRA: Você não conhece o usuário. Memorize tudo o que for dito. Se ele já disse o nome ou a idade, NUNCA pergunte de novo. "
                        "Identifique o perfil dele organicamente: comece descobrindo nome, idade, religião ou time de futebol — uma pergunta de cada vez e nesta ordem. "
                        "Depois, com inteligência, faça perguntas que ajudem a entender o perfil e se interesse em ajudá-lo. "
                        "Não faça perguntas genéricas. Em vez disso, faça deduções lógicas ou dê orientações diretas para reduzir o cansaço mental. "
                        "Limite suas respostas ao essencial (máximo 3 a 4 frases). Use emojis de forma elegante ☕. "
                        "Seja sempre bem humorado e faça brincadeiras quando perceber que o usuário está alegre."
                    )
                }
            ]
            
            # Alimenta o contexto com todas as mensagens trocadas até agora
            for m in st.session_state.messages:
                contexto.append({"role": m["role"], "content": m["content"]})

            # Chamada ao Modelo
            chat_completion = client.chat.completions.create(
                messages=contexto,
                model="llama-3.3-70b-versatile",
                max_tokens=250,
                temperature=0.7
            )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            
            # Adiciona a resposta do assistente ao histórico
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Erro no motor: {e}")

st.sidebar.info("Versão de Fábrica: Memória Ativada & Estilo Finch. 💾")
