import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Dashboard Clínico - Câncer de Mama",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTILIZAÇÃO CUSTOMIZADA (Fundo Geral Claro + Menu Idêntico à Imagem)
st.markdown("""
    <style>
    /* Fundo Principal em Branco */
    .stApp {
        background-color: #ffffff;
        color: #222222;
    }
    
    /* --- CONFIGURAÇÃO DO MENU (image_e49ecb.png) --- */
    
    /* Fundo Grafite Escuro da Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #1e2431 !important;
        border-right: none;
    }
    
    /* Remove o espaçamento padrão do Streamlit no topo do menu */
    [data-testid="stSidebar"] .st-emotion-cache-1c7ee8x, 
    [data-testid="stSidebar"] .st-emotion-cache-6qobix {
        padding-top: 0rem !important;
    }
    
    /* Bloco Azul do Topo */
    .menu-header-azul {
        background-color: #3b42f2;
        padding: 35px 20px;
        text-align: center;
        margin-top: -4rem; /* Força colar no topo absoluto */
        margin-left: -1.5rem;
        margin-right: -1.5rem;
        margin-bottom: 25px;
    }
    
    /* Ícone de Cruz Médica Customizado por CSS */
    .logo-cross {
        position: relative;
        width: 40px;
        height: 40px;
        margin: 0 auto;
    }
    .logo-cross::before, .logo-cross::after {
        content: "";
        position: absolute;
        background: #ffffff;
        border-radius: 4px;
    }
    /* Linha horizontal */
    .logo-cross::before {
        top: 14px; left: 0; width: 40px; height: 12px;
    }
    /* Linha vertical com efeito sombreado abaixo (conforme imagem) */
    .logo-cross::after {
        left: 14px; top: 0; width: 12px; height: 40px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Títulos de Seção (NAVIGATION, KPI FILTERS) */
    .menu-secao {
        color: #6e778a;
        font-size: 11px;
        font-weight: bold;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 25px 0px 15px 5px;
        font-family: sans-serif;
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
    p { color: #444444 !important; }
    </style>
""", unsafe_allow_html=True)


# 3. MENU LATERAL PERSONALIZADO (Estrutura da Imagem)
# Topo Azul com o Logo
st.sidebar.markdown("""
    <div class='menu-header-azul'>
        <div class='logo-cross'></div>
    </div>
""", unsafe_allow_html=True)

# Divisão de Navegação
st.sidebar.markdown(
    "<div class='menu-secao'>Navigation</div>", unsafe_allow_html=True)

# Opções de Navegação (Usando a seleção nativa do Streamlit com ícones correspondentes)
opcao = st.sidebar.radio(
    label="Navegação",
    options=["Summary", "Workforce", "Appointments",
             "Practice Ratings", "Performance", "Comparator"],
    label_visibility="collapsed"  # Esconde o label padrão do Streamlit
)

# Rodapé do Menu
st.sidebar.markdown(
    "<hr style='border-color: #2a3142; margin-top: 30px;'>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div class='menu-secao'>KPI Filters</div>", unsafe_allow_html=True)


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

    st.title("📊 Dashboard - Análise Exploratória de Dados")
    st.write(
        "Visão geral e distribuição das características clínicas da base de dados.")
    st.markdown("---")

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
        fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            <p style='color: #555566;'>Deseja realizar uma nova análise preditiva baseada neste comportamento clínico?</p>
            <a href="/1_Predicao" target="_self" style='background-color: #e91e63; color: white !important; padding: 12px 35px; text-decoration: none; font-weight: bold; border-radius: 6px; display: inline-block; box-shadow: 0 4px 15px rgba(233,30,99,0.3);'>Acessar Predição ➔</a>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erro ao construir o ambiente visual: {e}")
