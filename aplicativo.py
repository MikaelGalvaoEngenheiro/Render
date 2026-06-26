import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Dashboard Clínico - Câncer de Mama",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTILIZAÇÃO CUSTOMIZADA (Correção de sobreposição e alinhamento ao topo)
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
    
    /* REMOVE ELEMENTOS INVISÍVEIS DO STREAMLIT QUE CAUSAM SOBREPOSIÇÃO */
    [data-testid="stSidebar"] .stElementContainer:has(label[data-testid="stWidgetLabel"]-visible) {
        display: none !important;
    }
    /* Esconde elementos vazios gerados pelo radio oculto */
    div[data-testid="stRadio"] > label {
        display: none !important;
    }
    
    /* Zera os paddings nativos do container interno para o menu colar no topo */
    [data-testid="stSidebarContent"] {
        padding-top: 0rem !important;
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    
    /* Força o texto das opções nativas a ficarem brancos */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #ffffff !important;
    }
    
    /* Bloco do Topo Azul (Sem margem negativa quebrada, colado perfeitamente) */
    .menu-header-azul {
        background-color: #3b42f2;
        padding: 40px 20px;
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
    
    /* Título "MENU" em Branco */
    .menu-titulo {
        color: #ffffff !important;
        font-size: 14px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 20px 15px 15px 15px;
        font-family: sans-serif;
        border-bottom: 1px solid #2a2a30;
        padding-bottom: 8px;
    }
    
    /* Ajuste de espaçamento para as opções do Radio ficarem bonitas na barra */
    [data-testid="stSidebarUserContent"] div[data-testid="stRadio"] {
        padding-left: 15px;
        padding-right: 15px;
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


# 3. MENU LATERAL PERSONALIZADO (Ordem limpa e correta)
# 1º O Topo Azul colado acima de tudo
st.sidebar.markdown("""
    <div class='menu-header-azul'>
        <div class='logo-cross'></div>
    </div>
""", unsafe_allow_html=True)

# 2º O Título do Menu
st.sidebar.markdown("<div class='menu-titulo'>MENU</div>",
                    unsafe_allow_html=True)

# 3º As opções selecionáveis de forma limpa
opcao = st.sidebar.radio(
    label="Menu de Navegação",
    options=["📊 Dashboard", "🤖 Predição"],
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

    # Alterna o conteúdo principal dependendo da opção clicada no menu lateral
    if "Dashboard" in opcao:
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
            st.markdown(
                f"<div class='card-metrica'><div class='card-titulo'>Área Médica M.</div><div class='card-valor' style='color: #00897b;'>{area_med_mal:.1f}</div></div>", unsafe_allow_html=True)

        with col5:
            textura_med = df['texture_mean'].mean()
            st.markdown(
                f"<div class='card-metrica'><div class='card-titulo'>T. Média Tumor</div><div class='card-valor' style='color: #f57c00;'>{textura_med:.1f}</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráficos
        col_g1, col_g2 = st.columns(2)
        template_grafico = "plotly_white"

        with col_g1:
            st.subheader("Gráfico Pizza: Proporção")
            fig_pizza = px.pie(df, names='diagnosis', color='diagnosis', color_discrete_map={
                               'Benigno': '#1f77b4', 'Maligno': '#e91e63'}, hole=0.4, template=template_grafico)
            fig_pizza.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pizza, use_container_width=True)

        with col_g2:
            st.subheader("Box Plot: Distribuição de Área")
            fig_box = px.box(df, x='diagnosis', y='area_mean', color='diagnosis', color_discrete_map={'Benigno': '#1f77b4', 'Maligno': '#e91e63'}, labels={
                             'diagnosis': 'Diagnóstico', 'area_mean': 'Área Média (mm²)'}, template=template_grafico)
            fig_box.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_box, use_container_width=True)

    elif "Predição" in opcao:
        st.title("🤖 Análise Preditiva com Inteligência Artificial")
        st.write(
            "Insira os parâmetros clínicos para calcular a probabilidade de diagnóstico.")
        st.markdown("---")
        st.info("Área reservada para os inputs e outputs do seu modelo preditivo.")

except Exception as e:
    st.error(f"Erro ao construir o ambiente visual: {e}")
