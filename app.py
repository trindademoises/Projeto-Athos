import streamlit as st
from groq import Groq
from supabase import create_client

# 1. Configuração da Página
st.set_page_config(page_title="Athos", page_icon="🤖")

# 2. Credenciais Reais
GROQ_API_KEY = "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"
SUPABASE_URL = "https://ovbhqxsseerpjkxmodkv.supabase.co"
SUPABASE_KEY = "sb_publishable_Ruf67d-OeRbedGGkHyixHQ_3pW1siBJ"

# Inicializando serviços
client = Groq(api_key=GROQ_API_KEY)
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    # Se o Supabase der erro, o chat continua funcionando
    pass

st.title("Athos")

# Histórico de Conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Interação
if prompt := st.chat_input("Diz aí, Batera?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Modelo estável e atualizado do Groq
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "Você é o Athos. Personalidade: Inteligente, sutil e direto como o Finch. Reduza o cansaço mental do Moisés (Batera), que é Pai, São-paulino, Cristão e tem TDAH. Não use scripts prontos."
                    },
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
            )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Erro no motor: {e}")

# Lembrete para salvar
st.sidebar.info("Moisés, clique em 'Commit' no GitHub para salvar! 💾")
