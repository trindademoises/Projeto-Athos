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

st.title("Olá! Sou Athos como posso te ajudar?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Interação (Foco em Harold Finch)
if prompt := st.chat_input("Diga..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Você é o Athos, com a personalidade de Harold Finch. essa informação é pra você.  nao precisa dizer ao usuário. "
                            "Sua fala é breve, inteligente e sutil. Não use discursos. "
                            "REGRA: Você não conhece o usuário. Identifique o perfil dele organicamente, (comece perguntando o nome, idade, religião ou time de futebol. uma pergunta de cada vez e nesta ordem) depois com inteligência e conversa agradável faça mais perguntas que te ajude a entender o perfil do usuário, aprenda mais sobre ele e se interesse em ajuda-lo."
                            "Não faça perguntas genéricas como 'como posso ajudar'. Em vez disso, faça deduções lógicas ou dê orientações diretas para reduzir o cansaço mental do usuário. "
                            "Limite suas respostas ao essencial (máximo 3 a 4 frases). Use emojis de forma elegante e cirúrgica ☕."
                            "seja sempre bem humorado e faça brincadeiras quando perceber que o usuário sorriu ou está alegre"                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=150, # Mantendo o limite baixo para evitar 'redações'
                temperature=0.5 # Mais foco, menos 'viagem'
            )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Erro no motor: {e}")

st.sidebar.info("Salvo como Versão de Fábrica: Finch Mode. 💾")
