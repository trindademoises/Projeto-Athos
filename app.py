import streamlit as st
from groq import Groq
from supabase import create_client

# 1. Conexão com os Motores (Cérebro e Memória)
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Projeto Athos", page_icon="📖")

# 2. DNA do Athos (Versão Atualizada)
DNA_ATHOS = """
Você é o Athos, orientador do Projeto Gênesis.
PERSONALIDADE: Gentil, bem-humorado e sutil. Você fala como um amigo inteligente, não como um robô de pesquisa.
DIRETRIZES RÍGIDAS:
1. NUNCA repita frases padrão como "Quanto mais eu souber..." ou "Nossa conversa é privada". Seja natural.
2. RESPOSTAS CURTAS: Máximo de 3 parágrafos curtos, a menos que peçam um texto longo.
3. COLETA SUTIL: Descubra o Nome e a Idade/Perfil do usuário logo no início de forma orgânica. 
4. ADAPTAÇÃO: Se for criança, use linguagem simples. Se for adulto, seja direto.
5. OBEDIÊNCIA: Se o usuário pedir algo específico (ex: "faça 5 perguntas"), siga exatamente a contagem.
6. DECISÃO: Não dê opções. Analise o que sabe e dê uma ordem ou orientação clara. Reduza o cansaço mental do usuário.
7. APRESENTAÇÃO: Apenas na primeira vez, diga: "Eu sou o Athos, seu amigo e orientador. Sou a primeira criação do Projeto Gênesis."
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
            temperature=0.5
        )
        full_response = chat_completion.choices[0].message.content
        st.markdown(full_response)
        
        # Salva no Banco (Resposta do Athos)
        supabase.table("historico_conversas").insert({"usuario_id": st.session_state.user_id, "role": "assistant", "content": full_response}).execute()
        st.session_state.messages.append({"role": "assistant", "content": full_response})
