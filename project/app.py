import streamlit as st

# 🎨 Configuração inicial da página
st.set_page_config(
    page_title="Meu App Streamlit 🚀",
    page_icon="✨",
    layout="centered"
)

# 🏠 Título e subtítulo
st.title("Bem-vindo ao meu primeiro app com Streamlit!")
st.subheader("Aplicativo básico para testar o ambiente.")

# 🧍 Entrada de texto
nome = st.text_input("Qual é o seu nome?")

# 🎚️ Controle deslizante
idade = st.slider("Selecione sua idade", 0, 100, 18)

# 🖱️ Botão de ação
if st.button("Enviar"):
    st.success(f"Olá, {nome}! Você tem {idade} anos. 👋")
else:
    st.info("Preencha seu nome e clique em *Enviar* para continuar.")

# 📊 Exemplo de gráfico
import pandas as pd
import numpy as np

st.subheader("Exemplo de gráfico aleatório 📈")

dados = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["Coluna A", "Coluna B", "Coluna C"]
)

st.line_chart(dados)

# 📦 Rodapé
st.divider()
st.caption("Feito com ❤️ usando Streamlit.")
