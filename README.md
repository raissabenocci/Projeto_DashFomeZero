# Projeto Dashboard Fome Zero

Construção de dashboard utilizando o Python 3.11 para análise de dados, com base nos dados da Zomato Restaurants disponibilizados no Kaggle.

## 1. Problema de negócio

A empresa Fome Zero é uma marketplace de restaurantes, cujo core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

## 2. Premissas do negócio

### a. Fonte de dados
Os dados utilizados foram obtidos da [Zomato Restaurants - Autoupdated dataset no Kaggle](https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset/code), no dia 23/02/2024.
<br>Esta empresa contém informações dos top restaurantes das cidades mais importantes ao longo do mundo.

### b. Modelo de Negócio da origem dos dados
Assumiu-se que o modelo de negócio que deu origem aos dados era marketplace.

### c. Visões de Negócio
As visões de negócio foram geral, de países, de tipos de Culinária e de restaurantes. <br>

A ideia central foi ter um panorama geral da qualidade do serviço oferecido pelos restaurantes, considerando-se como dimensões dos dados:
- localização geográfica
- tipo de culinária
- categoria de preços do cardápio
- condições de delivery, pedido online e disponibilização de reservas.

Não foi realizada uma análise temporal, devido à ausência desta informação.

### d. Campos relevantes disponibilizados na base de dados
| Column | Description |
| :----- | :---------- |
| Restaurant ID | ID do restaurante | 
| Restaurant Name | Nome do Restaurante |
| Country Code | Código do País |
| City | Nome da Cidade onde o restaurante está |
| Longitude | Ponto geográfico de Longitude do Restaurante |
| Latitude | Ponto geográfico de Latitude do Restaurante |
| Cuisines | Tipos de Culinária servidos no restaurante |
| Average Cost for two   | Preço Médio de um prato para duas pessoas no restaurante |
| Currency | Moeda do país |
| Has Table booking | Se o restaurante possui serviços de reserva; 1 - Sim; 0 - Não |
| Has Online delivery | Se o restaurante possui serviços de pedido on-line; 1 - Sim; 0 - Não |
| Is delivering now | Se o restaurante faz entregas; 1 - Sim; 0 - Não |
| Price range | Variação de preços do restaurante; 1 a 4 - Quanto maior o valor, mais caro serão os pratos |
| Aggregate rating | Nota média do restaurante |
| Rating color | Código Hexadecimal da cor do restaurante com base em sua nota média |
| Rating text | Texto da categoria em que o restaurante está com base em sua nota média |
| Rating Category | Categoria em que o restaurante está com base em sua nota média |
| Votes | Quantidade de avaliações que o restaurante já recebeu |

## 3. Estratégia da solução
Como o CEO fictício tem interesse em conhecer o segmento e o comportamento geral dos restaurantes ao longo do mundo

## 4. Top 3 Insights de dados

Todas as categorias de custos dos cardápios possuem avaliações muito boas e também 

## 5. O Produto final do projeto
Dashboard online, hospedado na Streamlit Cloud, acessável publicamente.

O acesso online é possível através do link [https://dashboard-fomezero-app.streamlit.app/](https://dashboard-fomezero-app.streamlit.app/).

## 6. Conclusão

Os dados parecem bastante enviezados para estabelecimentos situados na Índia.

Teria sido interessante trazer qual era base do dolar no instante da liberação dos dados.
A maioria dos dados eram consistentes dentro de um mesmo país, com raros outliers para preço médio do prato para dois (por exemplo).

## 7. Próximos passos

Para novos releases dos dados, poderia haver a informação

## 8. Dúvidas e sugestões
Favor contactar Raíssa Thibes através do e-mail raissabenocci@gmail.com
