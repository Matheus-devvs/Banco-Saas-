-- Análise de Métricas SaaS (Streaming) com Python e PostgreSQL--


Este projeto nasceu da ideia de aprofundar meus estudos em análise de dados e SQL. Assim como fiz no meu projeto anterior de e-commerce, criei um cenário simulado — desta vez de uma plataforma de streaming — para praticar a extração e o cálculo de métricas de negócio usando Python conectado a um banco de dados relacional.

-- O cenário e o raciocínio para que as análises fizessem sentido, foi modelar o banco do zero dividindo os dados em quatro tabelas principais: clientes, planos, assinaturas e pagamentos.

Com essa base estruturada, busquei responder às perguntas mais comuns de uma operação SaaS:

 MRR: Quanto entra de receita recorrente considerando apenas os clientes ativos?
 Taxa de Churn: Qual a porcentagem de cancelamentos e quanto dinheiro isso representa?
 ARPU: Qual a receita média gerada por cada assinante ativo?
 LTV: Qual o valor estimado que um cliente deixa na empresa ao longo do tempo?
 Visão geral: Receita total acumulada e proporção de pagamentos efetivamente pagos.

Como os dados vêm de um banco estático que eu mesmo criei, os cálculos funcionam como um retrato atual da operação. Sei que no dia a dia de empresas maiores essas métricas exigem histórico temporal e análises de coorte mais complexas, mas o foco aqui foi dominar a lógica relacional e matemática por trás delas.

-- Ferramentas utilizadas e o porquê de cada uma

 PostgreSQL + Docker + DBeaver: Subi o banco em um container Docker para manter o ambiente isolado e usei o DBeaver para escrever e testar os scripts SQL (DDL/DML), definindo chaves primárias, estrangeiras e tipos de dados.

 SQLAlchemy e psycopg2: Foram usados para conectar o Python ao PostgreSQL e puxar as tabelas direto para o meu código.

 Pandas: Foi a base de toda a análise. Usei para filtrar status de assinaturas, cruzar tabelas com merge (fazendo o papel do JOIN) e calcular os indicadores.

 Plotly Express: Usei para gerar um gráfico comparando o MRR com o valor dos planos cancelados, facilitando a visualização dos números.

 Python-Dotenv: Usei para guardar usuário, senha e porta do banco em um arquivo .env, evitando deixar dados sensíveis expostos no código.
