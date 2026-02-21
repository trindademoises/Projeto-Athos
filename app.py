import streamlit as st
import streamlit.components.v1 as components

# 1. Configuração da Página e App Capability
st.set_page_config(
    page_title="Projeto Gênesis",
    page_icon="logo.png",
    layout="centered"
)

# Injeção para transformar em "App" no celular
components.html(
    """
    <script>
    const meta = document.createElement('meta');
    meta.name = "apple-mobile-web-app-capable";
    meta.content = "yes";
    window.parent.document.getElementsByTagName('head')[0].appendChild(meta);
    </script>
    """,
    height=0,
)

# 2. Exibição do Logo no Topo
st.image("logo.png", width=100)
st.title("Athos: Projeto Gênesis")

# --- Restante do seu código de chat aqui ---
