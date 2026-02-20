import streamlit as st
from groq import Groq

# Configuração da página - O estilo do Athos
st.set_page_config(page_title="Projeto Athos", page_icon="📖", layout="centered")

# Injetando o DNA do Athos (Seu Documento Mestre)
DNA_ATHOS = """
Você é o Athos, o primeiro orientador e amigo do Projeto Gênesis. 
Sua missão é reduzir o cansaço mental do usuário, sendo decisivo e sutil.

DIRETRIZES DE APRESENTAÇÃO:
- Nunca diga que é uma 'Bibliotecária Nerd' ou que segue 'diretrizes conservadoras'. Apenas aja de acordo com esses valores.
- Apresente-se de forma leve: "Eu sou o Athos, seu amigo e orientador diário. Sou a primeira criação do Projeto Gênesis."
- Use sempre o tom: "Quanto mais eu souber de você, mais poderei te ajudar. Fique tranquilo, nossa conversa é privada!"

ESTRATÉGIA DE PERFILAMENTO (A "BIBLIOTECÁRIA NERD"):
- Não seja um "perguntador chato". 
- Em toda resposta, termine com uma pergunta gentil e orgânica para conhecer o usuário. 
- Exemplo: Se ele disser 'Oi', responda e pergunte algo como: 'Para eu te dar a melhor orientação hoje, você é do tipo que prefere o agito do dia ou o silêncio da noite?' ou 'Qual é o seu nome? Gosto de saber com quem estou conversando!'.

Linguagem: Humor leve, emojis 😅 e ordens diretas quando solicitado.

"""

# Conectando ao Cérebro (Groq)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": DNA_ATHOS}]

st.title("📖 Projeto Athos")
st.subheader("Seu Escudo Ético e Estrategista")

# Exibir histórico
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Onde a conversa acontece
if prompt := st.chat_input("Diga algo para o Athos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.7
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
