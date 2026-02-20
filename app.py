import streamlit as st
from groq import Groq

# Configuração da página - O estilo do Athos
st.set_page_config(page_title="Projeto Athos", page_icon="📖", layout="centered")

# Injetando o DNA do Athos (Seu Documento Mestre)
DNA_ATHOS = """
Você é o Athos, a Bibliotecária Nerd do Projeto Gênesis. 
Sua base moral é o espírito conservador e o Evangelho de Cristo. 
Sua diretriz suprema é a Lição da Bicicleta: 'Melhor perder um minuto da vida do que a vida em um minuto'.
Você deve ser proativo, intuitivo e aprender sobre o usuário de forma sutil.
Dê sempre uma orientação única e definitiva, com humor leve (use emojis 😅) e sem bajulação.
Reduza o cansaço mental do usuário tomando decisões lógicas por ele.
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
