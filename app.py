import streamlit as st
from groq import Groq
from supabase import create_client

# Configuração da página
st.set_page_config(page_title="Athos", page_icon="🤖")

# Conexões (Recuperando do estado anterior)
# Substitua pelas suas chaves do Groq e Supabase que você já usava
GROQ_API_KEY = "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"
SUPABASE_URL = "https://ovbhqxsseerpjkxmodkv.supabase.co"
SUPABASE_KEY = "sb_publishable_Ruf67d-OeRbedGGkHyixHQ_3pW1siBJ"

client = Groq(api_key=GROQ_API_KEY)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Athos")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Diz aí, Batera?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # O motor Groq que não dá erro 404
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Você é o Athos, sutil e direto. Ajude o Moisés (Batera)."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-70b-8192",
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Erro: {e}")

st.sidebar.info("Moisés, voltamos para a estaca zero. Salva aí! 💾")
