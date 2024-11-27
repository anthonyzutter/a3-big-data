import pandas as pd
import plotly.express as px
import locale

# Configurar o locale para o Brasil (moeda em R$)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Caminho do arquivo CSV
arquivo_csv = '20240112_Despesas_Empenho.csv'

# Carregar o CSV com tratamento de codificação
data = pd.read_csv(arquivo_csv, delimiter=';', encoding='latin1')

# Listar as colunas carregadas para verificação
print("Colunas carregadas no DataFrame:")
print(data.columns.tolist())

# Pré-processamento
# Criar a coluna "Valor" a partir de "Valor do Empenho Convertido pra R$"
data['Valor'] = pd.to_numeric(data['Valor do Empenho Convertido pra R$'].str.replace(',', '.'), errors='coerce')

# Remover duplicatas
data_cleaned = data.drop_duplicates()

# Garantir que a coluna 'Data Emissão' seja tratada como datetime
data_cleaned['Data Emissão'] = pd.to_datetime(data_cleaned['Data Emissão'], errors='coerce')

# **Certifique-se de converter para string ou datetime diretamente no gráfico**
data_cleaned['Data Emissão'] = data_cleaned['Data Emissão'].dt.strftime('%Y-%m')  # Formato "YYYY-MM"

# Gráfico 1: Top 10 Favorecidos
top_favored = (
    data_cleaned.groupby('Favorecido', as_index=False)['Valor']
    .sum()
    .nlargest(10, 'Valor')
)

# Formatar os valores em reais
top_favored['Valor'] = top_favored['Valor'].apply(lambda x: locale.currency(x, grouping=True))

# Gráfico 1: Top 10 Favorecidos
favored_chart = px.bar(
    top_favored,
    x='Valor',
    y='Favorecido',
    orientation='h',
    title='Top 10 Favorecidos',
    labels={'Valor': 'Valor (R$)'},
    text_auto=True
)

# Gráfico 2: Valores por Órgão
orgao_data = (
    data_cleaned.groupby('Órgão', as_index=False)['Valor']
    .sum()
    .sort_values(by='Valor', ascending=True)
)

# Formatar os valores em reais para o gráfico de Órgão
orgao_data['Valor'] = orgao_data['Valor'].apply(lambda x: locale.currency(x, grouping=True))

orgao_chart = px.bar(
    orgao_data,
    x='Órgão',
    y='Valor',
    title='Valores por Órgão',
    labels={'Valor': 'Valor (R$)'},
    text_auto=True
)
orgao_chart.update_layout(xaxis_tickangle=-45)

# Gráfico 3: Distribuição por Categoria Econômica
categoria_economica_data = (
    data_cleaned.groupby('Categoria de Despesa', as_index=False)['Valor']
    .sum()
)

# Formatar os valores em reais para o gráfico de Categoria Econômica
categoria_economica_data['Valor'] = categoria_economica_data['Valor'].apply(lambda x: locale.currency(x, grouping=True))

categoria_economica_chart = px.bar(
    categoria_economica_data,
    x='Categoria de Despesa',
    y='Valor',
    title='Distribuição por Categoria Econômica',
    labels={'Valor': 'Valor (R$)'},
    text_auto=True
)

# Gráfico 4: Distribuição de valores por Categoria de Despesa (gráfico de pizza)
categoria_pie_chart = px.pie(
    data_cleaned,
    names='Categoria de Despesa',
    values='Valor',
    title='Distribuição de Valores por Categoria de Despesa',
    labels={'Valor': 'Valor (R$)', 'Categoria de Despesa': 'Categoria'}
)


# Exibir os gráficos
favored_chart.show()
orgao_chart.show()
categoria_economica_chart.show()
categoria_pie_chart.show() 
