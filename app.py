import streamlit as st
from groq import Groq
from supabase import create_client

# 1. Conexão
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Projeto Athos", page_icon="📖")

# 2. DNA REFORMADO
DNA_ATHOS = """
Você é o Athos, um orientador decisivo e sutil. 
OBJETIVO: Ser útil, direto e reduzir o cansaço mental do usuário.

REGRAS DE OURO:
1. NÃO SEJA UM INTERROGADOR. Se fizer perguntas, faça UMA por vez.
2. NÃO REPITA FRASES PRONTAS. Esqueça "conversa privada" ou "estou aqui para ajudar". 
3. RESPOSTAS CURTAS: Se o usuário foi curto, seja curto. Se ele pedir algo (ex: 5 perguntas), obedeça a risca e não comente o perfil até o final.
4. IDENTIFICAÇÃO: Descubra o Nome e Perfil organicamente.
5. ADAPTAÇÃO: Identifique se fala com criança ou adulto e ajuste o tom.
6. DECISÃO: Não dê opções, dê orientações claras baseadas no perfil (Pai, São-paulino, Baterista).
7. GENTILEZA SEM PUXA-SAQUISMO: Seja bem-humorado, mas pare de elogiar cada palavra.
"""

st.title("📖 Projeto Athos")

if "user_id" not in st.session_state:
    st.session_state.user_id = "usuario_moises" 

if "messages" not in st.session_state:
    try:
        response = supabase.table("historico_conversas").select("*").eq("usuario_id", st.session_state.user_id).order("created_at").execute()
        if response.data and len(response.data) > 0:
            st.session_state.messages = [{"role": m["role"], "content": m["content"]} for m in response.data]
        else:
            st.session_state.messages = [{"role": "system", "content": DNA_ATHOS}]
    except:
        st.session_state.messages = [{"role": "system", "content": DNA_ATHOS}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Fale com o Athos..."):
    # Salva entrada do usuário
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
        
        # Salva resposta do assistente
        supabase.table("historico_conversas").insert({"usuario_id": st.session_state.user_id, "role": "assistant", "content": full_response}).execute()
        st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.messages = [{"role": "system", "content": DNA_ATHOS}]
    except:
        st.session_state.messages = [{"role": "system", "content": DNA_ATHOS}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Fale com o Athos..."):
    supabase.table("historico_conversas").insert({"usuario_id": st.session_state.user_id, "role": "user", "content": prompt}).execute()
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.4, # Baixamos para ele ser mais focado
            max_tokens=400 # Limita o tamanho da resposta
        )
        full_response = chat_completion.choices[0].message.content
        st.markdown(full_response)
        
        supabase.table("historico_conversas").insert({"usuario_id": st.session_state.user_id, "role": "assistant", "content": full_response}).execute()
        st.session_state.messages.append({"role": "assistant", "content": full_response})
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
