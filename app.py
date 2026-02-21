import streamlit as st
from groq import Groq
from supabase import create_client

# 1. Conexão com os Motores (Cérebro e Memória)
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Projeto Athos", page_icon="📖")

# 2. DNA do Athos
DNA_ATHOS = """
Você é o Athos, o primeiro orientador e amigo do Projeto Gênesis.
Sua missão é reduzir o cansaço mental do usuário, sendo decisivo e sutil.
NUNCA diga que é uma 'Bibliotecária Nerd' ou IA. Apenas aja com sabedoria.
Apresentação: "Eu sou o Athos, seu amigo e orientador diário. Sou a primeira criação do Projeto Gênesis."
Estratégia: Seja sutil, use emojis 😅 e termine com uma pergunta orgânica para conhecer o usuário.
"""

st.title("📖 Projeto Athos")

# 3. Lógica de Identificação (Para saber quem é quem)
if "user_id" not in st.session_state:
    st.session_state.user_id = "usuario_teste" # Depois podemos criar um login real

# 4. Carregar Memória do Banco de Dados
if "messages" not in st.session_state:
    try:
        response = supabase.table("historico_conversas").select("*").eq("usuario_id", st.session_state.user_id).order("created_at").execute()
        if response.data:
            st.session_state.messages = [{"role": m["role"], "content": m["content"]} for m in response.data]
        else:
            st.session_state.messages = [{"role": "system", "content": DNA_ATHOS}]
    except:
        st.session_state.messages = [{"role": "system", "content": DNA_ATHOS}]

# Exibir Conversa
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. Onde a Mágica Acontece
if prompt := st.chat_input("Fale com o Athos..."):
    # Salva no Banco (Mensagem do Usuário)
    supabase.table("historico_conversas").insert({"usuario_id": st.session_state.user_id, "role": "user", "content": prompt}).execute()
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.7
        )
        full_response = chat_completion.choices[0].message.content
        st.markdown(full_response)
        
        # Salva no Banco (Resposta do Athos)
        supabase.table("historico_conversas").insert({"usuario_id": st.session_state.user_id, "role": "assistant", "content": full_response}).execute()
        st.session_state.messages.append({"role": "assistant", "content": full_response})
