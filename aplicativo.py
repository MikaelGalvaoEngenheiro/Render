import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA (Tema Escuro e Layout Amplo)
st.set_page_config(
    page_title="Dashboard Clínico - Câncer de Mama", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. ESTILIZAÇÃO CUSTOMIZADA (CSS para os Quadrados/Cards e Cores da Paleta)
st.markdown("""
    <style>
    /* Estilização dos blocos/quadrados superiores */
    .card-metrica {
        background-color: #1e1e2f;
        border: 1px solid #3a3a55;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
        margin-bottom: 15px;
    }
    .card-titulo {
        font-size: 14px;
        color: #a0a0b8;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .card-valor {
        font-size: 26px;
        color: #e91e63;
        font-weight: 250px;
    }
    
    /* Ajustes no menu lateral para fixar a paleta escura */
    [data-testid="stSidebar"] {
        background-color: #12121e;
    }
    </style>
""", unsafe_allow_html=True)

# 3. MENU LATERAL PERSONALIZADO (Navegação Nativa)
st.sidebar.markdown("<h2 style='color: #e91e63; font-weight: bold;'>Fit Health</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# 4. FUNÇÃO PARA CARREGAR OS DADOS
@st.cache_data
def carregar_dados():
    df = pd.read_csv('dados_tratados.csv')
    return df

try:
    df = carregar_dados()

    # Tratamento dos rótulos de diagnóstico
    if 'diagnosis' in df.columns:
        if df['diagnosis'].dtype == 'object':
            df['diagnosis'] = df['diagnosis'].map({'B': 'Benigno', 'M': 'Maligno', 'Benigno': 'Benigno', 'Maligno': 'Maligno'})
        else:
            df['diagnosis'] = df['diagnosis'].map({0: 'Benigno', 1: 'Maligno'})

    # TÍTULO PRINCIPAL DO DASHBOARD
    st.title("📊 Dashboard - Análise Exploratória de Dados")
    st.write("Visão geral e distribuição das características clínicas da base de dados.")
    st.markdown("---")

    # 5. ORGANIZAÇÃO DOS TEMPLATES: OS 5 QUADRADOS EM LINHA HORIZONTAL
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_benigno = len(df[df['diagnosis'] == 'Benigno'])
        st.markdown(f"<div class='card-metrica'><div class='card-titulo'>Benigno</div><div class='card-valor' style='color: #2b5c8f;'>{total_benigno}</div></div>", unsafe_allow_html=True)
        
    with col2:
        total_maligno = len(df[df['diagnosis'] == 'Maligno'])
        st.markdown(f"<div class='card-metrica'><div class='card-titulo'>Maligno</div><div class='card-valor'>{total_maligno}</div></div>", unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"<div class='card-metrica'><div class='card-titulo'>Qtd. Total</div><div class='card-valor' style='color: #ffffff;'>{len(df)}</div></div>", unsafe_allow_html=True)
        
    with col4:
        area_med_mal = df[df['diagnosis'] == 'Maligno']['area_mean'].mean()
        st.markdown(f"<div class='card-metrica'><div class='card-titulo'>Área Médica M.</div><div class='card-valor' style='color: #00bfa5;'>{area_med_mal:.1f}</div></div>", unsafe_allow_html=True)
        
    with col5:
        textura_med = df['texture_mean'].mean()
        st.markdown(f"<div class='card-metrica'><div class='card-titulo'>T. Média Tumor</div><div class='card-valor' style='color: #ffb300;'>{textura_med:.1f}</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 6. GRÁFICOS LADO A LADO (Conforme o esboço)
    col_g1, col_g2 = st.columns(2)

    # Definindo um tema escuro para os gráficos do Plotly
    template_grafico = "plotly_dark"

    with col_g1:
        st.subheader("Gráfico Pizza: Proporção")
        fig_pizza = px.pie(
            df, 
            names='diagnosis', 
            color='diagnosis', 
            color_discrete_map={'Benigno': '#2b5c8f', 'Maligno': '#e91e63'},
            hole=0.4,
            template=template_grafico
        )
        fig_pizza.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pizza, use_container_width=True)

    with col_g2:
        st.subheader("Box Plot: Distribuição de Área")
        fig_box = px.box(
            df, 
            x='diagnosis', 
            y='area_mean', 
            color='diagnosis',
            color_discrete_map={'Benigno': '#2b5c8f', 'Maligno': '#e91e63'},
            labels={'diagnosis': 'Diagnóstico', 'area_mean': 'Área Média (mm²)'},
            template=template_grafico
        )
        fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    # 7. BOTÃO COMPLEMENTAR DE REDIRECIONAMENTO
    st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            <p style='color: #a0a0b8;'>Deseja realizar uma nova análise preditiva baseada neste comportamento clínico?</p>
            <a href="/1_Predicao" target="_self" style='background-color: #e91e63; color: white !important; padding: 12px 35px; text-decoration: none; font-weight: bold; border-radius: 6px; display: inline-block; box-shadow: 0 4px 15px rgba(233,30,99,0.4);'>Acessar Predição ➔</a>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erro ao construir o ambiente visual: {e}")