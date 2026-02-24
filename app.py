import streamlit as st
from groq import Groq
from supabase import create_client

# 1. ESTÉTICA, IDENTIDADE E APP (PWA)
LOGO_PATH = "logo.png"
st.set_page_config(page_title="Athos", page_icon=LOGO_PATH, layout="centered")

# CSS para interface limpa e o azul bebê que você escolheu
st.markdown(f"""
    <style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    [data-testid="stImage"] {{ display: flex; justify-content: center; margin: 0 auto; }}
    .main-title {{ text-align: center; font-size: 45px; font-weight: bold; margin-top: -10px; color: white; }}
    .sub-title {{ text-align: center; font-size: 18px; font-style: italic; color: #5dade2; margin-bottom: 30px; }}
    /* Esconde botões de debug do Streamlit */
    .stDeployButton {{display:none;}}
    </style>
    <link rel="manifest" href="./manifest.json">
    """, unsafe_allow_html=True)

# Cabeçalho Centralizado
col1, col2, col3 = st.columns([1,1,1])
with col2:
    try: st.image(LOGO_PATH, width=150)
    except: pass

st.markdown('<div class="main-title">Athos</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Vamos conversar?</div>', unsafe
