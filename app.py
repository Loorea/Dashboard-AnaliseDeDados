import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard | Salary | Data Analysis",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

st.sidebar.header("Filtros")

# Construcao dos filtros (Ano, Experiencia, Contrato, Tamanho da empresa)
available_year = sorted(df['ano'].unique())
selected_year = st.sidebar.multiselect("Ano", available_year, default=available_year)

available_experience = sorted(df['senioridade'].unique())
selected_experience = st.sidebar.multiselect("Experiencia", available_experience, default=available_experience)

available_contract = sorted(df['contrato'].unique())
selected_contract = st.sidebar.multiselect("Tipo de Contrato", available_contract, default=available_contract)

available_size = sorted(df['tamanho_empresa'].unique())
selected_size = st.sidebar.multiselect("Tamanho da Empresa", available_size, default=available_size)

df_filtrado = df[
    (df['ano'].isin(selected_year)) &
    (df['senioridade'].isin(selected_experience)) &
    (df['contrato'].isin(selected_contract)) &
    (df['tamanho_empresa'].isin(selected_size))
]

st.title("Dashboard de Análise Salarial na Area de Dados")
st.markdown("Explore os dados salariais de profissionais da área de dados em varios paises. Utilize-se dos filtros na barra lateral para personalizar sua visualização dos dados.")

st.subheader("Metricas Gerais (Salario Anual em USD)")

if not df_filtrado.empty:
    average_salary = df_filtrado['usd'].mean()
    max_salary = df_filtrado['usd'].max()
    total_records = df_filtrado.shape[0]
    frequent_position = df_filtrado['cargo'].mode()[0]
else:
    average_salary = 0
    max_salary = 0
    total_records = 0
    frequent_position = "N/A"

col1, col2, col3, col4 = st.columns(4)

col1.metric("Salario Anual Medio (USD)", f"${average_salary:,.2f}")
col2.metric("Salario Anual Maximo (USD)", f"${max_salary:,.2f}")
col3.metric("Total de Registros", f"{total_records:,}")
col4.metric("Cargo Mais Frequente", frequent_position)

st.markdown("---")

st.subheader("Graficos")
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_positions = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        positions_graph = px.bar(
            top_positions,
            x='usd',
            y='cargo',
            orientation='h',
            title='Top 10 Cargos com Maior Salario Medio Anual (USD)',
            labels={'usd': 'Salario Medio Anual (USD)', 'cargo': ''},
            color_discrete_sequence=["#B40E02"]
        )
        positions_graph.update_layout(title_x=0.2, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(positions_graph, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de cargos.")
        
with col_graf2:
    if not df_filtrado.empty:
        hist_graph = px.histogram(
            df_filtrado,
            x='usd',
            title='Distribuição Salarial Anual (USD)',
            labels={'usd': 'Faixa Salarial (USD)', 'count': ''},
            color_discrete_sequence=["#B40E02"]
        )
        hist_graph.update_layout(title_x=0.2)
        st.plotly_chart(hist_graph, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o histograma salarial.")
    
col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remote_count = df_filtrado['remoto'].value_counts().reset_index()
        remote_count.columns = ['tipo_trabalho', 'quantidade']
        remote_graph = px.pie(
            remote_count,
            values='quantidade',
            names='tipo_trabalho',
            title='Distribuição de Trabalho Remoto vs Presencial',
            labels={'tipo_trabalho': 'Tipo de Trabalho', 'quantidade': 'Quantidade'},
            color_discrete_sequence=["#B40E02"],
            hole=0.5
        )
        remote_graph.update_traces(textposition='inside', textinfo='percent+label')
        remote_graph.update_layout(title_x=0.2)
        st.plotly_chart(remote_graph, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de trabalho remoto.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        med_country = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        contry_graph = px.choropleth(med_country,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='reds',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        contry_graph.update_layout(title_x=0.1)
        st.plotly_chart(contry_graph, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
