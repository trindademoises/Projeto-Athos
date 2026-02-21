import streamlit as st
from groq import Groq
from supabase import create_client

# 1. Conexão com os Motores
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Projeto Athos", page_icon="📖")

# 2. DNA do Athos
DNA_ATHOS = """
Você é o Athos, um orientador decisivo e sutil.
PERSONALIDADE: Gentil, bem-humorado e direto. Amigo inteligente.
DIRETRIZES:
1. SEM REPETIÇÕES: Não use frases como "conversa privada" ou "estou aqui para ajudar".
2. RESPOSTAS CURTAS: Se o usuário for breve, seja breve. Máximo 3 parágrafos.
3. OBEDIÊNCIA: Se pedirem 5 perguntas, faça uma por vez e NÃO comente o perfil até o fim.
4. IDENTIFICAÇÃO: Descubra Nome e Idade/Fase de vida organicamente.
5. DECISÃO: Reduza o cansaço mental. Dê orientações claras.
"""

st.title("📖 Projeto Athos")

if "user_id" not in st.session_state:
    st.session_state.user_id = "usuario_moises"

# 3. Carregar Histórico
if "messages" not in st.session_state:
    try:
        response = supabase.table("historico_conversas").select("*").eq("usuario_id", st.session_state.user_id).order("created_at").execute()
        if response.data and len(response.data) > 0:
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

# 4. Processar Nova Mensagem
if prompt := st.chat_input("Fale com o Athos..."):
    supabase.table("historico_conversas").insert({"usuario_id": st.session_state.user_id, "role": "user", "content": prompt}).execute()
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.4,
            max_tokens=400
        )
        full_response = chat_completion.choices[0].message.content
        st.markdown(full_response)
        
        supabase.table("historico_conversas").insert({"usuario_id": st.session_state.user_id, "role": "assistant", "content": full_response}).execute()
        st.session_state.messages.append({"role": "assistant", "content": full_response})
