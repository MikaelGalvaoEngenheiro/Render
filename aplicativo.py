import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import numpy as np

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Dashboard Clínico - Câncer de Mama",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CARREGAR O MODELO DE IA (KNN)


@st.cache_resource
def carregar_modelo():
    with open('modelo_knn.pkl', 'rb') as f:
        modelo = pickle.load(f)
    return modelo


try:
    model = carregar_modelo()
except Exception as e:
    st.error(f"Erro ao carregar o arquivo modelo_knn.pkl: {e}")
    st.stop()

# 3. ESTILIZAÇÃO CUSTOMIZADA
st.markdown("""
    <style>
    /* Força o cabeçalho nativo superior do Streamlit a ficar transparente/branco */
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    
    /* Fundo Principal em Branco */
    .stApp {
        background-color: #ffffff;
        color: #222222;
    }
    
    /* --- CONFIGURAÇÃO DO MENU LATERAL (COLADO NO TOPO) --- */
    [data-testid="stSidebar"] {
        background-color: #121214 !important;
        border-right: none;
    }
    
    /* Zera margens, paddings e caixas internas da barra lateral nativa */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    [data-testid="stSidebar"] section[data-testid="stSidebarUserContent"] > div:first-child:empty {
        display: none !important;
    }
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] {
        display: none !important;
    }
    div[data-testid="stRadio"] > label {
        display: none !important;
    }
    
    /* Força o contêiner interno a colar no topo absoluto (0px) */
    [data-testid="stSidebarContent"] {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    
    /* Alvo específico das classes de cache do Streamlit para zerar paddings superiores */
    .st-emotion-cache-1c7ee8x, .st-emotion-cache-6qobix {
        padding-top: 0rem !important;
    }
    
    [data-testid="stSidebarUserContent"] {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        margin-top: 0rem !important;
    }
    
    /* Bloco do Topo Azul - Sem margem superior para colar no teto */
    /* ============================
  /* =======================
   BLOCO AZUL DO TOPO
======================= */
.menu-header-azul{
    background:#3b42f2 !important;

    /* Faz o azul ocupar toda a largura */
    width:calc(100% + 32px) !important;

    /* Compensa o padding da sidebar */
    margin-left:-16px !important;
    margin-right:-16px !important;

    /* Desce o bloco para aparecer o botão << */
    margin-top:18px !important;
    margin-bottom:30px !important;

    height:170px;

    display:flex;
    justify-content:center;
    align-items:center;

    padding:0 !important;

    border-radius:0 !important;
}
    .logo-cross{
    position:relative;
    width:42px;
    height:42px;
    margin:auto;
}

.logo-cross::before,
.logo-cross::after{
    content:"";
    position:absolute;
    background:#fff;
    border-radius:4px;
}

.logo-cross::before{
    width:42px;
    height:10px;
    top:16px;
    left:0;
}

.logo-cross::after{
    width:10px;
    height:42px;
    left:16px;
    top:0;
}
    .logo-cross::before, .logo-cross::after {
        content: "";
        position: absolute;
        background: #ffffff;
        border-radius: 3px;
    }
    .logo-cross::before { top: 13px; left: 0; width: 36px; height: 10px; }
    .logo-cross::after { left: 13px; top: 0; width: 10px; height: 36px; }
    
    /* Título "CARDÁPIO" */
    .menu-titulo {
        color: #ffffff !important;
        font-size: 15px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 20px 20px 15px 20px;
        font-family: sans-serif;
        border-bottom: 1px solid #2a2a30;
        padding-bottom: 10px;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #ffffff !important;
        font-size: 15px !important;
    }
    [data-testid="stSidebarUserContent"] div[data-testid="stRadio"] {
        padding-left: 20px;
        padding-right: 20px;
    }


    /* Cards do Painel */
    .card-metrica {
        background-color: #000000; /* Alterado para preto */
        border: 1px solid #3b42f2; /* Opcional: borda na cor azul para combinar */
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    .card-titulo {
        font-size: 14px;
        color: #ffffff;;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .card-valor {
        font-size: 26px;
        color: #e91e63;
        font-weight: bold;
    }
    .main p { color: #444444 !important; }

    /* Estilização da aba de predição */
    .titulo-predicao { color: #3b42f2 !important; font-weight: bold !important; margin-top: 10px; }
    .subtitulo-secao { color: #3b42f2 !important; font-weight: bold !important; margin-top: 20px; margin-bottom: 10px; }
    
    /* Botão Azul customizado */
div.stButton > button:first-child {
    background-color: #3b42f2 !important; /* MUDADO PARA AZUL */
    color: white !important;
    font-weight: bold !important;
    border-radius: 6px !important;
    border: none !important;
    width: 100% !important;
    padding: 12px !important;
    box-shadow: 0 4px 15px rgba(59, 66, 242, 0.4); /* SOMBRA MUDADA PARA AZUL (RGBA) */
    transition: 0.3s;
}
    div.stButton > button:first-child:hover {
        background-color: #c2185b !important;
        box-shadow: 0 4px 20px rgba(233,30,99,0.6);
    }
    /* --- BOTÕES MODERNOS DE NAVEGAÇÃO --- */
div[data-testid="stSidebar"] button {
    background-color: #1e1e24 !important; /* Fundo do botão cinza escuro */
    color: #ffffff !important;
    border: 1px solid #2a2a30 !important;
    border-radius: 8px !important;
    padding: 12px 20px !important;
    width: 90% !important;
    margin: 0 auto 10px auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
    font-weight: 500 !important;
}

/* Efeito de passar o mouse (Hover) nos botões da barra lateral */
    div[data-testid="stSidebar"] button:hover {
        background-color: #7b2cbf !important; /* Muda para o roxo ao passar o mouse */
        border-color: #7b2cbf !important;
        color: #ffffff !important;
        /* Efeito de sombra brilhante (glow) em Roxo Neon */
        box-shadow: 0px 0px 20px rgba(138, 43, 226, 0.8) !important; 
        transform: translateY(-2px); /* Leve efeito de subir o botão */
    }

/* Estilo do botão quando estiver selecionado/ativo */
.botao-ativo button {
    background-color: #3b42f2 !important;
    border-color: #3b42f2 !important;
    font-weight: bold !important;
}
    </style>
""", unsafe_allow_html=True)

# 4. MENU LATERAL PERSONALIZADO
st.sidebar.markdown("""
    <div class='menu-header-azul'>
        <div class='logo-cross'></div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='menu-titulo'>NAVEGAÇÃO</div>", unsafe_allow_html=True)

# Inicializa a opção padrão se ela não existir no sistema ainda
if 'opcao' not in st.session_state:
    st.session_state.opcao = " Painel"

# Recuo visual nas laterais dos botões
st.sidebar.markdown("<div style='padding: 0 10px;'>", unsafe_allow_html=True)

# Botão 1: Painel
if st.session_state.opcao == " Painel":
    st.sidebar.markdown("<div class='botao-ativo'>", unsafe_allow_html=True)
if st.sidebar.button("  Dashboard Clínico", key="btn_painel"):
    st.session_state.opcao = " Painel"
    st.rerun()
if st.session_state.opcao == " Painel":
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Botão 2: Predição
if st.session_state.opcao == " Predição":
    st.sidebar.markdown("<div class='botao-ativo'>", unsafe_allow_html=True)
if st.sidebar.button("  Análise IA (KNN)", key="btn_predicao"):
    st.session_state.opcao = " Predição"
    st.rerun()
if st.session_state.opcao == " Predição":
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Atribui o estado atual para a variável 'opcao' que o resto do seu código já usa
opcao = st.session_state.opcao

# 5. FUNÇÃO PARA CARREGAR OS DADOS
@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados_tratados.csv')
    return df

try:
    df = carregar_dados()

    if 'diagnosis' in df.columns:
        # Garante que o texto seja lido como string e remove espaços extras (como 'M ' ou ' B')
        df['diagnosis'] = df['diagnosis'].astype(str).str.strip()
        
        # Faz o mapeamento exato de B e M para os nomes por extenso
        df['diagnosis'] = df['diagnosis'].map({'B': 'Benigno', 'M': 'Maligno', 'Benigno': 'Benigno', 'Maligno': 'Maligno'})

    # --- ABA 1: PAINEL ---
    if "Painel" in opcao:
        st.markdown("<h1 style='text-align: center; color: #222222;'>Dashboard Clínico - Análise Exploratória de Dados</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #222222; font-size: 24px;'>Visão geral da distribuição das características clínicas da base de dados.</p>", unsafe_allow_html=True)
        st.markdown("<hr style='border: 1px solid #000000;'>", unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            total_benigno = len(df[df['diagnosis'] == 'Benigno'])
            st.markdown(
                f"<div class='card-metrica'><div class='card-titulo'>Benigno</div><div class='card-valor' style='color: #1f77b4;'>{total_benigno}</div></div>", unsafe_allow_html=True)

        with col2:
            total_maligno = len(df[df['diagnosis'] == 'Maligno'])
            st.markdown(
                f"<div class='card-metrica'><div class='card-titulo'>Maligno</div><div class='card-valor'>{total_maligno}</div></div>", unsafe_allow_html=True)

        with col3:
            st.markdown(
                f"<div class='card-metrica'><div class='card-titulo'>Qtd. Total</div><div class='card-valor' style='color: #199013;'>{len(df)}</div></div>", unsafe_allow_html=True)

        with col4:
            area_med_mal = df[df['diagnosis'] == 'Maligno']['area_mean'].mean()
            st.markdown(
                f"<div class='card-metrica'><div class='card-titulo'>Área Médica M.</div><div class='card-valor' style='color: #00897b;'>{area_med_mal:.1f}</div></div>", unsafe_allow_html=True)

        with col5:
            textura_med = df['texture_mean'].mean()
            st.markdown(
                f"<div class='card-metrica'><div class='card-titulo'>T. Média Tumor</div><div class='card-valor' style='color: #f57c00;'>{textura_med:.1f}</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_g1, col_g2 = st.columns(2)
        template_grafico = "plotly_white"

        with col_g1:
            # Título alterado para HTML visando a centralização na coluna
            st.markdown("<h3 style='text-align: center; margin-bottom: 10px;'>Gráfico Pizza: Proporção</h3>", unsafe_allow_html=True)
            fig_pizza = px.pie(df, names='diagnosis', color='diagnosis', color_discrete_map={
                               'Benigno': '#1f77b4', 'Maligno': '#e91e63'}, hole=0.4, template=template_grafico)
            fig_pizza.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pizza, use_container_width=True)

        with col_g2:
            # Título alterado para HTML visando a centralização na coluna
            st.markdown("<h3 style='text-align: center; margin-bottom: 10px;'>Plot de Caixa: Distribuição de Área</h3>", unsafe_allow_html=True)
            fig_box = px.box(df, x='diagnosis', y='area_mean', color='diagnosis', color_discrete_map={'Benigno': '#1f77b4', 'Maligno': '#e91e63'}, labels={
                             'diagnosis': 'Diagnóstico', 'area_mean': 'Área Média (mm²)'}, template=template_grafico)
            fig_box.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                font=dict(color="#000000") 
            )
            st.plotly_chart(fig_box, use_container_width=True)

   # --- ABA 2: PREDIÇÃO COM MODELO KNN ---
    elif "Predição" in opcao:
        # Mantido em uma linha contínua para evitar quebras de string do interpretador Python
        st.markdown("<h1 class='titulo-predicao' style='text-align: center;'> Análise Preditiva com Inteligência Artificial</h1>", unsafe_allow_html=True)
        
        # MUDANÇA AQUI: Adicionado o font-size: 20px; no estilo abaixo
        st.markdown("<p style='text-align: center; color: #3b42f2; font-size: 20px;'>Preencha os 30 parâmetros clínicos abaixo para calcular a probabilidade de diagnóstico automatizado.</p>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 1px solid #000000;'>", unsafe_allow_html=True)

        with st.form("form_predicao"):

            # --- BLOCO 1: VALORES MÉDIOS ---
            st.markdown("<h3 class='subtitulo-secao'>Valores Médios</h3>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                v1 = st.number_input("Raio (Média)", value=14.0, format="%.4f")
                v4 = st.number_input("Área (Média)", value=650.0, format="%.2f")
                v7 = st.number_input("Concavidade (Média)", value=0.08, format="%.4f")
            with col2:
                v2 = st.number_input("Textura (Média)", value=19.0, format="%.4f")
                v5 = st.number_input("Suavidade (Média)", value=0.09, format="%.4f")
                v8 = st.number_input("Pontos Côncavos (Média)", value=0.04, format="%.4f")
            with col3:
                v3 = st.number_input("Perímetro (Média)", value=92.0, format="%.2f")
                v6 = st.number_input("Compacidade (Média)", value=0.10, format="%.4f")
                v9 = st.number_input("Simetria (Média)", value=0.18, format="%.4f")

            v10 = st.number_input("Dimensão Fractal (Média)", value=0.06, format="%.4f")

            st.markdown("---")

            # --- BLOCO 2: ERRO PADRÃO ---
            st.markdown("<h3 class='subtitulo-secao'>Erro Padrão</h3>", unsafe_allow_html=True)
            col4, col5, col6 = st.columns(3)
            with col4:
                v11 = st.number_input("Raio (Erro Padrão)", value=0.40, format="%.4f")
                v14 = st.number_input("Área (Erro Padrão)", value=40.0, format="%.2f")
                v17 = st.number_input("Concavidade (Erro Padrão)", value=0.03, format="%.4f")
            with col5:
                v12 = st.number_input("Textura (Erro Padrão)", value=1.21, format="%.4f")
                v15 = st.number_input("Suavidade (Erro Padrão)", value=0.006, format="%.5f")
                v18 = st.number_input("Pontos Côncavos (Erro Padrão)", value=0.01, format="%.4f")
            with col6:
                v13 = st.number_input("Perímetro (Erro Padrão)", value=2.86, format="%.2f")
                v16 = st.number_input("Compacidade (Erro Padrão)", value=0.02, format="%.4f")
                v19 = st.number_input("Simetria (Erro Padrão)", value=0.02, format="%.4f")

            v20 = st.number_input("Dimensão Fractal (Erro Padrão)", value=0.003, format="%.5f")

            st.markdown("---")

            # --- BLOCO 3: PIORES VALORES ---
            st.markdown("<h3 class='subtitulo-secao'>Piores Valores</h3>", unsafe_allow_html=True)
            col7, col8, col9 = st.columns(3)
            with col7:
                v21 = st.number_input("Raio (Pior Cenário)", value=16.2, format="%.4f")
                v24 = st.number_input("Área (Pior Cenário)", value=880.0, format="%.2f")
                v27 = st.number_input("Concavidade (Pior Cenário)", value=0.27, format="%.4f")
            with col8:
                v22 = st.number_input("Textura (Pior Cenário)", value=25.6, format="%.4f")
                v25 = st.number_input("Suavidade (Pior Cenário)", value=0.13, format="%.4f")
                v28 = st.number_input("Pontos Côncavos (Pior Cenário)", value=0.11, format="%.4f")
            with col9:
                v23 = st.number_input("Perímetro (Pior Cenário)", value=107.0, format="%.2f")
                v26 = st.number_input("Compacidade (Pior Cenário)", value=0.25, format="%.4f")
                v29 = st.number_input("Simetria (Pior Cenário)", value=0.29, format="%.4f")

            v30 = st.number_input("Dimensão Fractal (Pior Cenário)", value=0.08, format="%.4f")

            st.markdown("<br>", unsafe_allow_html=True)
            botao_prever = st.form_submit_button("Prever Resultado")

        espaco_resultado = st.container()

        if botao_prever:
            dados_entrada = np.array([[
                v1, v2, v3, v4, v5, v6, v7, v8, v9, v10,
                v11, v12, v13, v14, v15, v16, v17, v18, v19, v20,
                v21, v22, v23, v24, v25, v26, v27, v28, v29, v30
            ]])

            predicao = model.predict(dados_entrada)

            with espaco_resultado:
                st.markdown("---")
                if predicao[0] == 1 or predicao[0] == 'M' or predicao[0] == 'Maligno':
                    st.error("🚨 **Resultado da Predição: Maligno (M)**")
                    st.warning("A análise matemática identificou padrões compatíveis com tecidos tumorais malignos. Encaminhar para revisão médica detalhada.")
                else:
                    st.success("✅ **Resultado da Predição: Benigno (B)**")
                    st.info("A análise matemática identificou padrões associados a estruturas células benignas.")

except Exception as e:
    st.error(f"Erro ao construir o ambiente visual: {e}")