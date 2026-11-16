#Importação das bibliotecas necessárias para a análise do banco de dados.
import os
from dotenv import load_dotenv 
from sqlalchemy import create_engine 
import pandas as pd
import plotly.express as px

#Carregamento das variáveis de ambiente do arquivo .env para a conexão com o banco de dados.
load_dotenv() 

#Definição das variáveis de conexão com o banco de dados, utilizando as variáveis de ambiente carregadas. extraidas no postgres(dbeaver) e armazenadas no arquivo .env.
usuario = os.getenv("DB_USER")
senha = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
nome_banco = os.getenv("DB_NAME")

#Criação da URL de conexão com o banco de dados PostgreSQL, utilizando o driver psycopg2 e as variáveis de conexão definidas anteriormente.
url_conexao = f"postgresql+psycopg2://{usuario}:{senha}@{host}:{port}/{nome_banco}"

#Criação do engine de conexão com o banco de dados, utilizando a URL de conexão definida anteriormente.
engine = create_engine(url_conexao)

#--------------------------------------------------------------------------------------

#Teste e visualização das tabelas do banco de dados.

# df_planos = pd.read_sql("SELECT * FROM tb_planos;", engine)
# print("---planos---")
# print(df_planos.head(), "\n")

# df_clientes = pd.read_sql("SELECT * FROM tb_clientes;", engine)
# print("---clientes---")
# print(df_clientes.head(), "\n")

# df_assinaturas = pd.read_sql("SELECT * FROM tb_assinaturas;", engine)
# print ("---assinaturas---")
# print(df_assinaturas.head(), "\n")

# df_pagamentos = pd.read_sql("SELECT * FROM tb_pagamentos;", engine)
# print("---pagamentos---")      
# print(df_pagamentos.head(), "\n")   

#-------------------------------------------------------------------------------------- 

#Seleção dos dados das tabelas do banco de dados para análise das métricas do projeto Saas.

df_planos = pd.read_sql("SELECT * FROM tb_planos;", engine)
df_assinaturas = pd.read_sql("SELECT * FROM tb_assinaturas;", engine)
df_pagamentos = pd.read_sql("SELECT * FROM tb_pagamentos;", engine)
df_clientes = pd.read_sql("SELECT * FROM tb_clientes;", engine)

# --------------------------------------------------------------------------------------

#Cálculo do MMR (Monthly Recurring Revenue), que é a receita recorrente mensal, ou seja, a soma dos valores mensais das assinaturas ativas.

assinaturas_ativas = df_assinaturas[df_assinaturas['status_assinatura'] == 'ativa']
pd_mmr = pd.merge(assinaturas_ativas, df_planos, left_on = 'id_plano', right_on = 'id_plano')
mmr_total = pd_mmr['valor_mensal'].sum()

print ("---MMR TOTAL---")
print(f"MMR total: R$ {mmr_total:,.2f}")

soma_assinaturas = len(df_assinaturas)
total_ativos = len(assinaturas_ativas)

tx_mmr_percent = (total_ativos / soma_assinaturas) * 100
print(f"MMR total %: {tx_mmr_percent:.2f}%")

# --------------------------------------------------------------------------------------

#Cálculo da taxa de cancelamento, que é a soma dos valores mensais das assinaturas canceladas.

assinaturas_canceladas = df_assinaturas[df_assinaturas['status_assinatura'] == 'cancelada']
pd_cancelados = pd.merge(assinaturas_canceladas, df_planos, left_on = 'id_plano', right_on = 'id_plano')
tx_cancelados = pd_cancelados['valor_mensal'].sum()

print ("---TAXA DE CHURN---")
print(f"TX Cancelados: R$ {tx_cancelados:,.2f}")


# --------------------------------------------------------------------------------------

#Cálculo da taxa de churn, que é a proporção de clientes que cancelaram suas assinaturas em relação ao total de clientes.

soma_assinaturas = len(df_assinaturas)
total_cancelados = len(assinaturas_canceladas)

tx_churn = (total_cancelados / soma_assinaturas) * 100
print ("---TAXA DE CHURN---")
print(f"TX Churn: {tx_churn:.2f}%")

# --------------------------------------------------------------------------------------

#Cálculo da receita total, que é a soma de todos os pagamentos realizados pelos clientes.

receita_total = df_pagamentos['valor_pago'].sum()
print ("---RECEITA TOTAL---")
print(f"Receita total: R$ {receita_total:,.2f}")

soma_pagamentos = len(df_pagamentos)
total_pagamentos = len(df_pagamentos[df_pagamentos['status_pagamento'] == 'pago'])
tx_receita_percent = (total_pagamentos / soma_pagamentos) * 100
print(f"Percentual receita: {tx_receita_percent:.2f}%")

#--------------------------------------------------------------------------------------

#Cálculo do ARPU (Average Revenue Per User), que é a receita média por usuário ativo.

arpu = mmr_total / len(assinaturas_ativas)
print ("---ARPU---")
print(f"ARPU: R$ {arpu:,.2f}")

#--------------------------------------------------------------------------------------
 
 #Cálculo do LTV (Lifetime Value), tempo de vida do cliente, que é o valor que um cliente gera durante o tempo em que permanece ativo na empresa.

churn_decimal = tx_churn / 100

if churn_decimal > 0:
    ltv = arpu / churn_decimal
    print ("---LTV(Lifetime Value)---")
    print(f"LTV estimado: R$ {ltv:,.2f}")

else: 
    print("Não é possível calcular o LTV, pois a taxa de churn é zero.")


#--------------------------------------------------------------------------------------


#VISUALIZAÇÃO DAS MÉTRICAS EM GRAFICO 

dados_dashboard = {
    'Métrica': ['MMR Total', 'TX Cancelados'],
    'valor': [mmr_total, tx_cancelados]
}

df_plot = pd.DataFrame(dados_dashboard)

fig = px.bar(
    df_plot,
    x='Métrica',
    y='valor',
    title='Dashboard de Métricas do Projeto Saas',
    text_auto=',.2f',
    color='Métrica',

)

fig.show()