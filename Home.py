# # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #    PRE-ÂMBULO DO CÓDIGO   # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #  
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Importar libraries
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from itables import init_notebook_mode
init_notebook_mode( all_interactive=True )
import time
#
import base64  # Add this line to import the base64 module
#
import inflection  # after installing in Miniconda using:  conda install conda-forge::inflection
#
from haversine import haversine  # para calcular a distância entre dois pontos geográficos
#
import os
#os.add_dll_directory('C:\\Users\\HCInsula\\Miniconda\\DLLs')  # para dar certo as dependências
from os.path import exists
#
import streamlit as st   # to display things in Streamlit API
import folium                               # to things on maps
from streamlit_folium import folium_static  # to indeed show the map
from folium.plugins import MarkerCluster
#
from PIL import Image    # to bring images to show in StreamLit
#
from datetime import datetime  # to work with dates and times
#
from io import BytesIO
#
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Page settings  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
st.set_page_config( page_title='Home' , page_icon='icons/home.png' , layout="wide" )
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Funções
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
# --------------------------------- -------------------------------- ------------------------ Função para Nome dos Países
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
#
def country_name( country_id ):
    ''' FUNCTION takes the country id and uses it
        as the index to find the country name
    '''
    return COUNTRIES[ country_id ]
#
# --------------------------------- -------------------------------- ------------------------ Função para criação do Tipo de Categoria de Comida
def create_price_type( price_range ):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
#
# --------------------------------- -------------------------------- ------------------------ Função para criação do nome das Cores
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
#
def color_name( color_code ):
    return COLORS[ color_code ]
#
# --------------------------------- -------------------------------- ------------------------ Função para renomear as colunas do DataFrame
def rename_columns( dataframe ):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_new = list( df.columns )                     # initialize cols_new with "old" columns name
    cols_new = list(  map( title,     cols_new )  )   # capitalize words
    cols_new = list(  map( spaces,    cols_new )  )   # take spaces off
    cols_new = list(  map( snakecase, cols_new )  )   # put underscore between lower case followed by upper case
    df.columns = cols_new
    return df
#
# --------------------------------- -------------------------------- ------------------------ Função definir a categoria de avaliação
def rating_category( aggregate_rating ):
    '''  FUNÇÃO  define qual é a categoria de avaliação baseado em alguns limite
    Input: aggregate_rating
    Output: categoria de rating, na forma de um texto
    '''
    if aggregate_rating >= 4.5:
        rate_categ = 'Excelente'
    elif aggregate_rating >= 4 and aggregate_rating < 4.5:
        rate_categ = 'Muito Bom'
    elif aggregate_rating >= 3.5 and aggregate_rating < 4:
        rate_categ = 'Bom'
    elif aggregate_rating >= 2.5 and aggregate_rating < 3.5:
        rate_categ = 'Razoável'
    elif aggregate_rating >= 0.1 and aggregate_rating < 2.5:
        rate_categ = 'Ruim'
    else:
        rate_categ = 'Sem avaliação'
    #
    return rate_categ
#
#  --------------------------------- -------------------------------- ------------------------   Limpeza e preparação dos dados
def clean_data( df ):
    ''' FUNÇÃO para limpeza e renomeamento de dados
    '''
    # Change columns names
    df1 = rename_columns( df )
    #
    # Change variable typesif False:
    # # Verifying dtypes
    # print( df1.dtypes )
    #
    # '''
    #     Floats should be:
    #         longitude
    #         latitude
    #         average_cost_for_two
    #         aggregate_rating
    
    #     ! There are no problems if these are Integers
   
    
    #     Integers should be:
    #         votes
    
    
    #     Should be Strings but ! ! there are no problems if are Integers:
    #         restaurant_id
    #         country_code
    #         has_table_booking
    #         has_online_delivery
    #         is_delivering_now
    #         switch_to_order_menu
    #         price_range
    # '''
    #
    #
    # # Trick to verify all unique() values of all columns that are supposedly categories
    if False:
        print( '\nVerifing  unique values . . .\n' )
        for columnName in df1.columns:
            valsUnique = df1[ columnName ].sort_values(ascending=True, na_position='first').unique()
            if len( valsUnique ) <= 15:
                print( columnName, '  -       ', valsUnique )
    #
    #
    # # Fix cuisines
    # como tem mais de um tipo de culinária, a sugestão do cientista de dados pleno foi
    # selecionar somente por um tipo de culinária
    df1["cuisines"] = df1["cuisines"].fillna("NaN")
    df1["cuisines"] = df1.loc[ : , "cuisines"].apply(lambda x: x.split(",")[0] if x else "NaN")
    #
    # Create Country Names column
    df1['country_names']    = df1.loc[ : , 'country_code'     ].apply( lambda x: country_name(x) )
    #
    # Create Rating Category
    df1["rating_category"]  = df1.loc[ : , "aggregate_rating" ].apply(lambda x: rating_category(x) )
    #
    # Create Price Type column
    df1["price_type"]       = df1.loc[ : , "price_range"      ].apply(lambda x: create_price_type(x) )
    #
    # Create Color Names column
    df1["color_name"]       = df1.loc[ : , "rating_color"     ].apply(lambda x: color_name(x) )
    #
    # Drop duplicates
    df1 = df1.drop_duplicates()
    #
    # Drop Na rows
    df1 = df1.dropna()
    #
    return df1
#
# --------------------------------- -------------------------------- ------------------------    Plot   Map chart  com folium
def map_visao_geografica_restaurantes( df1 ):  
    """ FUNÇÃO que cria a variável map contendo as coordenadas com as medianas da posição geográfica dos restaurante
        Agregação feita por 
        Input:  Dataframe
        Output: map
    """
    df_aux = ( df1.loc[:,['restaurant', 'restaurant_name', 'city', 'average_cost_for_two', 'currency',
                       'longitude', 'latitude', 'cuisines', 'color_name', 'aggregate_rating' ]]
               .groupby(['restaurant']).max().reset_index() )
    #
    map = folium.Map()
    marker_cluster = MarkerCluster( name="restaurantes" ).add_to( map )
    #
    def cor(rating_name):
        cores = df_aux.iloc[ rating_name , 8 ]
        # print( cores )
        return cores
        
    for _, df_row in df_aux.iterrows():
        #
        name          = df_row["restaurant_name"]
        price_for_two = df_row["average_cost_for_two"]
        cuisine       = df_row["cuisines"]
        currency      = df_row["currency"]
        rating        = df_row["aggregate_rating"]
        maxScore      = 5
        ratingPerc    = np.round( rating/maxScore , 2)*100
        color         = f'{df_row["color_name"]}'
        #
        html = "<p><strong>{}</strong></p>"
        html += "<p>Price prato para dois: {},00 {}"
        html += "<br />Type: {}"
        html += "<br />Aggregate Rating: {}/5.0"
        html += " - {}%"
        html = html.format(name, price_for_two, currency, cuisine, rating, ratingPerc)
        #
        popup = folium.Popup(
            folium.Html( html , script=True ),
            max_width=500,
        )
        #
        folium.Marker(
            [df_row["latitude"], df_row["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to( marker_cluster )
        #
    #    
    # Display the map
    folium_static( map , width=1024, height=600)
    #
    return None
#
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Aviso do horário de execução do .py
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
print( '\n\nCurrent time:', datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
print( "\nUsuário acessou a página :  Home\n\n" )
#
#
# # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #    INÍCIO DA ESTRUTURA LÓGICA DO CÓDIGO   # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Carregar os dados da tabela
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
df = pd.read_csv( 'dataset/zomato.csv' )
df1 = df.copy()
print( 'colunas:\n', sorted( list( df1 )) )
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Limpar os dados
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
df1 = clean_data( df1 )
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Ajustes no Dataframe
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Change columns names
df1 = rename_columns( df1 )
#
#
print( "Inicialmente,  havia ", len( df ) , "linhas na base" )
print( "Após limpeza do df possui ", len( df1 ) , "linhas na base" )
#
print( 'colunas:\n', sorted( list( df1 )) )
#
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Layout de visão no StreamLit para dashboards
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
with st.spinner('Aguarde...'):
    time.sleep(5)
#st.success('Done!')
#
# Headers 1
with st.container():
    col1,col2 = st.columns( 2 )
    with col1:
        #markdown_content = f'<h1 style="text-align: center; color:#f54647"> Fome Zero </h1>'
        #markdown_content += f'<h3 style="text-align: center;"> O Melhor lugar para encontrar seu mais novo restaurante favorito! </h3>'  % #f54647
        markdown_content = """
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 30vh; background-color:tomato;">
            <h1 style="text-align: center; color:white;">Fome Zero</h1> 
            <h3 style="text-align: center; color:#ffcccc">O Melhor lugar para encontrar seu mais novo restaurante favorito!</h3>
        </div>
        """
        st.markdown( markdown_content , unsafe_allow_html = True )
    with col2:
        image_path = 'restaurant.jpeg'
        # image = Image.open( image_path )  # st.image( image, width=800, caption='Fonte: https://commons.wikimedia.org/wiki/File:Tom%27s_Restaurant,_NYC.jpg' )
        markdown_content = f'<p style="text-align: center; font-size:60%; color:gray;"><img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: 270px; margin-right: 20px;"> <br> Modificado de: https://commons.wikimedia.org/wiki/File:Tom%27s_Restaurant,_NYC.jpg</p>'
        st.markdown( markdown_content , unsafe_allow_html = True )
#
# Headers 2 + métricas de negócio
with st.container():
    #
    st.markdown( """---""" )
    markdown_content = """
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 30vh; background-color:tomato;">
        <h1 style="text-align: center; color:white;">Fome Zero</h1> 
        <h3 style="text-align: center; color:#ffcccc">O Melhor lugar para encontrar seu mais novo restaurante favorito!</h3>
    </div>
    """
    markdown_content = f'<h3 style="margin-left: 10%; ">Informações gerais sobre os restaurantes da nossa plataforma<br><br></h3>'
    st.markdown( markdown_content , unsafe_allow_html = True )
    # st.markdown( "### Informações gerais sobre os restaurantes da nossa plataforma:" )
#
#
# ============================================================================================================================== Sidebar
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Imagem e Header
image_path = 'comidas.jpg'
image = Image.open( image_path )
#st.sidebar.image( image, width=120 )
markdown_content = f'<h1 style="text-align: center;"><img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: 55px; margin-right: 20px;">   Fome Zero </h1>'
st.sidebar.markdown(  markdown_content , unsafe_allow_html = True  )
#
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Filtros da Sidebar
st.sidebar.markdown( """---""" )
st.sidebar.markdown( '## Filtros' )
#
st.sidebar.markdown( '### Escolha as opções para visualizar os Restaurantes' )
#
countriesOptions = st.sidebar.multiselect(
    'Países:',
    sorted( list( df1['country_names'].unique() )),
    ['Australia','Brazil','Canada','England','Qatar','South Africa'] )
#
#
cuisinesOptions = st.sidebar.multiselect(
    'Tipos de Culinária:',
    sorted( list( df1['cuisines'].unique() )),
    ['Brazilian','Japanese','Home-made'] )
#
#
st.sidebar.markdown( "Adicionar Restaurantes que:" )
onlineOrder  = st.sidebar.checkbox( 'Aceitam pedidos online' ,   value=True )
delivery     = st.sidebar.checkbox( 'Realizam delivery' ,        value=True )
tableBooking = st.sidebar.checkbox( 'Realizam reserva da mesa' , value=True )
# if agree:
#     st.sidebar.write('Great!')
#
st.sidebar.markdown( """---""" )
#
#
st.sidebar.markdown( """---""" )
#
#
# Fechamento do sidebar
# st.sidebar.markdown( """---""" )
# st.sidebar.markdown( 'Powered by CDS - Raíssa Thibes' )
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Aplicação de Filtro
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Backup sem filtro
dfarc = df1.copy()
# print( '\nColunas da dfarc:\n', sorted( list(dfarc)) )
# print( '\nColunas da df1:\n', sorted( list(df1)) )
# print( dfarc['restaurant'] , '\n\n' )
#
# Filtro de condição de transito
linhas_selecionadas = df1['country_names'].isin( countriesOptions )
df1 = df1.loc[ linhas_selecionadas, : ]
print( "\nApós aplicar filtro,  há ", len( df1 ) , "linhas na base\n" )
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Visualizações das análises
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
with st.container():
    col1, col2, col3, col4, col5 = st.columns( 5 )
    with col1:
        df_aux = dfarc.loc[ dfarc['restaurant'] != 'NaN'    , : ]
        amountRest = len( df_aux.loc[ :, 'restaurant'].unique()  )
        col1.metric( 'Restaurantes', amountRest)
    with col2:
        df_aux = dfarc.loc[ dfarc['country_code'] != 'NaN'  , : ]
        amountCountry = len( df_aux.loc[ : , 'country_code' ].unique()  )
        col2.metric( 'Países', amountCountry)
    with col3:
        df_aux = dfarc.loc[ dfarc['city'] !='NaN'  , :]
        amountCity = len( df_aux.loc[ : , 'city' ].unique() )
        col3.metric( 'Cidades' , amountCity )
    with col4:
        cols = ['restaurant','votes']
        df_aux = dfarc.loc[ dfarc['votes'] != 'NaN' , cols ]
        amountVotes = df_aux['votes'].sum()
        # Format the metric value with Brazilian Portuguese conventions
        formatted_amountVotes = str( "{:,.0f}".format(amountVotes) ).replace( ',' , '.' )
        col4.metric( 'Avaliações feitas na plataforma' , formatted_amountVotes)
    with col5:
        df_aux = dfarc.loc[ dfarc['cuisines'] != 'NaN' , :]
        amountCuisines =  len( df_aux['cuisines'].unique() )
        col5.metric( 'Tipos de Culinária' , amountCuisines )
#

with st.container():
    markdown_content = f'<h3 style="text-align: center; margin-right: 20%;"> <br>Restaurantes pelo mundo </h3>'
    st.markdown( markdown_content , unsafe_allow_html=True )
    map = map_visao_geografica_restaurantes( df1 )
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Roda pé da página
#
st.markdown( f'<p> <br> </p>', unsafe_allow_html=True )
st.markdown( """---""" )
st.markdown( f'Base de dados : {len( df )} linhas' )
st.markdown(
    '''
    Fome Zero Dashboard foi construído para acompanhar a quantidade de restaurantes cadastrados ao longo do mundo.
    ##### Páginas do dashboard?
    - Restaurantes por Países
    - Restaurantes por Cidades
    - Restaurantes por Tipos de Culinária
    ##### Ask for help
        Contactar Raíssa Thibes no Discord 
        @raissa.thibes
    ''' 
)
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
