import streamlit as st
from groq import Groq
from supabase import create_client

# 1. ESTÉTICA E IDENTIDADE
LOGO_PATH = "logo.png" 

st.set_page_config(page_title="Athos", page_icon=LOGO_PATH, layout="centered")

# CSS Ajustado: Centraliza a logo e remove menus/header
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Centraliza a imagem da logo */
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-left: auto;
        margin-right: auto;
    }
    
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-top: 10px;
    }
    .sub-title {
        text-align: center;
        font-size: 14px;
        font-style: italic;
        color: gray;
        margin-bottom: 20px;
    }
    .sub-title a {
        color: #5dade2;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho Centralizado
try:
    st.image(LOGO_PATH, width=150) # Logo acima de tudo
except:
    pass

st.markdown('<div class="main-title">Athos</div>', unsafe_allow_html=True)

# Link SEGURO: Apenas a URL do seu app, sem informações de gerenciamento
st.markdown('<div class="sub-title">Para add o Athos na sua tela principal <a href="https://projeto-athos.streamlit.app/" target="_blank">clique aqui</a>.</div>', unsafe_allow_html=True)

# --- RESTANTE DO CÓDIGO (Credenciais, Supabase e Motor) MANTIDOS IGUAIS ---
