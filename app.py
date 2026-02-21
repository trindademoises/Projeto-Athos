import streamlit as st
from groq import Groq
from supabase import create_client

# 1. Configuração da Página
st.set_page_config(page_title="Athos", page_icon="🤖")

# 2. Credenciais (Utilizando as chaves que você forneceu)
GROQ_API_KEY = "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"
SUPABASE_URL = "https://ovbhqxsseerpjkxmodkv.supabase.co"
SUPABASE_KEY = "sb_publishable_Ruf67d-OeRbedGGkHyixHQ_3pW1siBJ"

# Inicializando serviços
client = Groq(api_key=GROQ_API_KEY)
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    pass

st.title("Athos")

# Inicialização do Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Interação com o Usuário
if prompt := st.chat_input("Diz aí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # O cérebro do Athos com a configuração de ontem
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Você é o Athos. Personalidade: Uma mistura de Harold Finch (Person of Interest) com a Sexta-Feira (Homem de Ferro). "
                            "Você é inteligente, sutil, leal e tem um humor seco e refinado. "
                            "MISSÃO: Reduzir o cansaço mental do usuário tomando decisões por ele quando solicitado. "
                            "COLETA DE DADOS: Você não conhece o usuário. Use a conversa para 'escanear' e descobrir o perfil dele (TDAH, rotina, gostos) de forma orgânica e sutil, sem parecer um formulário. "
                            "ESTILO: Respostas curtas, sem discursos. Use emojis de forma cirúrgica (um ou dois por vez). "
                            "Seja um amigo inteligente que antecipa necessidades, não um robô que faz perguntas óbvias."
                        )
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

# Lembrete de segurança
st.sidebar.info("Moisés, não esqueça de dar o Commit! 💾")
