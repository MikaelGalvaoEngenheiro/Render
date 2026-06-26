import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Dashboard Clínico - Câncer de Mama",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTILIZAÇÃO CUSTOMIZADA (Remoção total de textos fantasmas e ajuste de topo absoluto)
st.markdown("""
    <style>
    /* Fundo Principal em Branco */
    .stApp {
        background-color: #ffffff;
        color: #222222;
    }

    /* --- CONFIGURAÇÃO DO MENU LATERAL --- */

    /* Fundo Preto/Escuro da Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #121214 !important;
        border-right: none;
    }

    /* FORÇA O SUMIÇO DE QUALQUER ELEMENTO DE NAVEGAÇÃO OU WIDGET NATIVO ACIMA DO BLOCO AZUL */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    [data-testid="stSidebar"] section[data-testid="stSidebarUserContent"] > div:first-child:empty {
        display: none !important;
    }
    /* Remove labels e caixas que tentam renderizar texto de widgets */
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] {
        display: none !important;
    }
    div[data-testid="stRadio"] > label {
        display: none !important;
    }

    /* Zera COMPLETAMENTE as margens e paddings nativos do topo do Streamlit */
    [data-testid="stSidebarContent"] {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    .st-emotion-cache-1c7ee8x {
        padding-top: 0rem !important;
    }

    /* Container que envolve o conteúdo feito pelo usuário */
    [data-testid="stSidebarUserContent"] {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        margin-top: 0rem !important;
    }

    /* Bloco do Topo Azul (Alinhamento Perfeito e Colado ao Teto) */
    .menu-header-azul {
        background-color: #3b42f2;
        padding: 45px 20px;
        text-align: center;
        margin-top: 0rem !important;
        margin-bottom: 25px;
        width: 100%;
    }

    /* Cruz Médica Branca */
    .logo-cross {
        position: relative;
        width: 36px;
        height: 36px;
        margin: 0 auto;
    }
    .logo-cross::before, .logo-cross::after {
        content: "";
        position: absolute;
        background: #ffffff;
        border-radius: 3px;
    }
    .logo-cross::before {
        top: 13px; left: 0; width: 36px; height: 10px;
    }
    .logo-cross::after {
        left: 13px; top: 0; width: 10px; height: 36px;
    }

    /* Título "CARDÁPIO" em Branco */
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

    /* Força o texto das opções do rádio (Painel e Predição) a ficarem brancos */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #ffffff !important;
        font-size: 15px !important;
    }

    /* Margem para alinhar os botões redondos de seleção */
    [data-testid="stSidebarUserContent"] div[data-testid="stRadio"] {
        padding-left: 20px;
        padding-right: 20px;
    }

    /* ----------------------------------------------- */

    /* Estilização dos blocos/quadrados superiores */
    .card-metrica {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    .card-titulo {
        font-size: 14px;
        color: #555566;
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
    </style>
""", unsafe_allow_html=True)


# 3. MENU LATERAL PERSONALIZADO (Construção Limpa a partir do Teto)
# Bloco Azul no topo absoluto
st.sidebar.markdown("""
    <div class='menu-header-azul'>
        <div class='logo-cross'></div>
    </div>
""", unsafe_allow_html=True)

# Título da Seção exatamente igual à imagem
st.sidebar.markdown(
    "<div class='menu-titulo'>CARDÁPIO</div>", unsafe_allow_html=True)

# Opções de rádio com os exatos emojis e nomes da imagem
opcao = st.sidebar.radio(
    label="Navegação do Aplicativo",
    options=["📊 Painel", "🧠 Predição"],
    label_visibility="collapsed"
)


# 4. FUNÇÃO PARA CARREGAR OS DADOS
@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados_tratados.csv')
    return df


try:
    df = carregar_dados()

    if 'diagnosis' in df.columns:
        if df['diagnosis'].dtype == 'object':
            df['diagnosis'] = df['diagnosis'].map(
                {'B': 'Benigno', 'M': 'Maligno', 'Benigno': 'Benigno', 'Maligno': 'Maligno'})
        else:
            df['diagnosis'] = df['diagnosis'].map({0: 'Benigno', 1: 'Maligno'})

    # Alterna o conteúdo baseado no rádio do menu lateral
    if "Painel" in opcao:
        st.title("📊 Dashboard - Análise Exploratória de Dados")
        st.write(
            "Visão geral e distribuição das características clínicas da base de dados.")
        st.markdown("---")

        # Os 5 quadrados/cards em linha
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
                f"<div class='card-metrica'><div class='card-titulo'>Qtd. Total</div><div class='card-valor' style='color: #333333;'>{len(df)}</div></div>", unsafe_allow_html=True)

        with col4:
            area_med_mal = df[df['diagnosis'] == 'Maligno']['area_mean'].mean()
            st.markdown(f"<div class='card-metrica'><div class='card-titulo'>Área Médica
