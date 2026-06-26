import streamlit as st
import pandas as pd
import pickle
import numpy as np

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Predição - Fit Health", layout="wide")

# 2. CARREGAR O MODELO DE IA (KNN)


@st.cache_resource
def carregar_modelo():
    # Carrega o arquivo pkl que está na raiz do seu projeto
    with open('modelo_knn.pkl', 'rb') as f:
        modelo = pickle.load(f)
    return modelo


try:
    model = carregar_modelo()
except Exception as e:
    st.error(f"Erro ao carregar o arquivo modelo_knn.pkl: {e}")
    st.stop()

# 3. ESTILIZAÇÃO DA PALETA ESCURA E BOTÃO ROSA
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #12121e; }
    h2, h3 { color: #e91e63 !important; font-weight: bold !important; }
    div.stButton > button:first-child {
        background-color: #e91e63 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        border: none !important;
        width: 100% !important;
        padding: 10px !important;
        box-shadow: 0 4px 15px rgba(233,30,99,0.4);
    }
    </style>
""", unsafe_allow_html=True)

# TÍTULOS
st.markdown("<h2 style='text-align: center;'>Predição de Câncer de Mama</h2>",
            unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0a0b8;'>Preencha os 30 parâmetros clínicos abaixo para realizar o diagnóstico automatizado</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. CRIANDO O FORMULÁRIO COM OS 30 PARÂMETROS ORGANIZADOS
with st.form("form_predicao"):

    # --- BLOCO 1: VALORES MÉDIOS ---
    st.markdown("<h3>Valores Médios</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        v1 = st.number_input("Raio (Média)", value=14.0, format="%.4f")
        v4 = st.number_input("Área (Média)", value=650.0, format="%.2f")
        v7 = st.number_input("Concavidade (Média)", value=0.08, format="%.4f")
    with col2:
        v2 = st.number_input("Textura (Média)", value=19.0, format="%.4f")
        v5 = st.number_input("Suavidade (Média)", value=0.09, format="%.4f")
        v8 = st.number_input("Pontos Côncavos (Média)",
                             value=0.04, format="%.4f")
    with col3:
        v3 = st.number_input("Perímetro (Média)", value=92.0, format="%.2f")
        v6 = st.number_input("Compacidade (Média)", value=0.10, format="%.4f")
        v9 = st.number_input("Simetria (Média)", value=0.18, format="%.4f")

    v10 = st.number_input("Dimensão Fractal (Média)",
                          value=0.06, format="%.4f")

    st.markdown("---")

    # --- BLOCO 2: ERRO PADRÃO ---
    st.markdown("<h3>Erro Padrão</h3>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    with col4:
        v11 = st.number_input("Raio (Erro Padrão)", value=0.40, format="%.4f")
        v14 = st.number_input("Área (Erro Padrão)", value=40.0, format="%.2f")
        v17 = st.number_input("Concavidade (Erro Padrão)",
                              value=0.03, format="%.4f")
    with col5:
        v12 = st.number_input("Textura (Erro Padrão)",
                              value=1.21, format="%.4f")
        v15 = st.number_input("Suavidade (Erro Padrão)",
                              value=0.006, format="%.5f")
        v18 = st.number_input(
            "Pontos Côncavos (Erro Padrão)", value=0.01, format="%.4f")
    with col3 if 'col6' not in locals() else col6:
        v13 = st.number_input("Perímetro (Erro Padrão)",
                              value=2.86, format="%.2f")
        v16 = st.number_input("Compacidade (Erro Padrão)",
                              value=0.02, format="%.4f")
        v19 = st.number_input("Simetria (Erro Padrão)",
                              value=0.02, format="%.4f")

    v20 = st.number_input("Dimensão Fractal (Erro Padrão)",
                          value=0.003, format="%.5f")

    st.markdown("---")

    # --- BLOCO 3: PIORES VALORES ---
    st.markdown("<h3>Piores Valores</h3>", unsafe_allow_html=True)
    col7, col8, col9 = st.columns(3)
    with col7:
        v21 = st.number_input("Raio (Pior Cenário)", value=16.2, format="%.4f")
        v24 = st.number_input("Área (Pior Cenário)",
                              value=880.0, format="%.2f")
        v27 = st.number_input("Concavidade (Pior Cenário)",
                              value=0.27, format="%.4f")
    with col8:
        v22 = st.number_input("Textura (Pior Cenário)",
                              value=25.6, format="%.4f")
        v25 = st.number_input("Suavidade (Pior Cenário)",
                              value=0.13, format="%.4f")
        v28 = st.number_input(
            "Pontos Côncavos (Pior Cenário)", value=0.11, format="%.4f")
    with col9:
        v23 = st.number_input("Perímetro (Pior Cenário)",
                              value=107.0, format="%.2f")
        v26 = st.number_input("Compacidade (Pior Cenário)",
                              value=0.25, format="%.4f")
        v29 = st.number_input("Simetria (Pior Cenário)",
                              value=0.29, format="%.4f")

    v30 = st.number_input("Dimensão Fractal (Pior Cenário)",
                          value=0.08, format="%.4f")

    st.markdown("<br>", unsafe_allow_html=True)

    # BOTÃO DE SUBMISSÃO
    botao_prever = st.form_submit_button("Prever Resultado")

# 5. PROCESSAMENTO DA PREDIÇÃO AO CLICAR NO BOTÃO
if botao_prever:
    # Organiza os dados na ordem exata que o KNN espera (30 colunas)
    dados_entrada = np.array([[
        v1, v2, v3, v4, v5, v6, v7, v8, v9, v10,
        v11, v12, v13, v14, v15, v16, v17, v18, v19, v20,
        v21, v22, v23, v24, v25, v26, v27, v28, v29, v30
    ]])

    # Realiza o cálculo usando o arquivo PKL
    predicao = model.predict(dados_entrada)

    st.markdown("---")
    # Exibe o resultado de forma elegante
    if predicao[0] == 1 or predicao[0] == 'M':
        st.error("🚨 **Resultado da Predição: Maligno (M)**")
        st.warning("A análise matemática identificou padrões compatíveis com tecidos tumorais malignos. Encaminhar para revisão médica detalhada.")
    else:
        st.success("✅ **Resultado da Predição: Benigno (B)**")
        st.info(
            "A análise matemática identificou padrões associados a estruturas celulares benignas.")
