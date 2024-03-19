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
init_notebook_mode(all_interactive=True)
#
import base64  # Add this line to import the base64 module
#
import inflection  # after installing in Miniconda using:  conda install conda-forge::inflection
#
# Set the locale to Brazilian Portuguese -  this allows the thousando separator to be '.' and the decimal separator ','
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
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
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
#
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Page settings
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
st.set_page_config(   page_title='Countries'  ,  page_icon='icons/globe.png'  ,  layout="wide" )
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
# --------------------------------- -------------------------------- ------------------------ Função definir a categoria de avaliação
def create_price_type( price_range ):
    '''  FUNÇÃO  define qual é a categoria de preços do restaurante
    Input: price_range
    Output: price_type: categoria de preço, na forma de um texto
    '''
    if  price_range == 1:
        price_type = 'Cheap'
    elif price_range == 2:
        price_type = 'Normal'
    elif price_range == 3:
        price_type = 'Expensive'
    elif price_range == 4:
        price_type = 'Gourmet'
    #
    return price_type#
#
#  --------------------------------- -------------------------------- ------------------------   Limpeza e preparação dos dados
def clean_data( df ):
    ''' FUNÇÃO para limpeza e renomeamento de dados
    '''
    # Change columns names
    df1 = rename_columns( df )
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
    df1['country_names']   = df1.loc[ : , 'country_code'     ].apply( lambda x: country_name(x) )
    #
    # Create Rating Category
    df1["rating_category"] = df1.loc[ : , "aggregate_rating" ].apply(lambda x: rating_category(x) )
    #
    # Create Price Type column
    df1["price_type"]      = df1.loc[ : , "price_range"      ].apply(lambda x: create_price_type(x) )
    #
    # Create Color Names column
    df1["color_name"]       = df1.loc[ : , "rating_color"     ].apply(lambda x: color_name(x) )
    #
    df1['booking']      = df1.loc[ : , 'has_table_booking'    ].apply( lambda x: 'Reserva' if x==1 else 'Imediata' )
    df1['online_order'] = df1.loc[ : , 'has_online_delivery'  ].apply( lambda x: 'Online' if x==1 else 'Pessoalmente' )
    df1['delivery']     = df1.loc[ : , 'is_delivering_now'    ].apply( lambda x: 'Entrega' if x==1 else 'Sem entrega' )
    #
    # Drop duplicates
    df1 = df1.drop_duplicates()
    #
    # Drop Na rows
    df1 = df1.dropna()
    #
    return df1
#
#
#  --------------------------------- -------------------------------- ------------------------    Listar  de Restaurantes  tipo de cardápio + reserva  +  delivery  +  pedido online
def show_bestrestaurants_listaGourmetExpensive( tiposCardapio , df1 ):
    '''  FUNÇÃO Lista os Restaurantes [ Gourmet ]
         com [Reserva]                     em ranking de [melhor avaliação] e de [maior Preço para Dois]
         ou     Lista os Restaurantes [ Expensive ]
         com [Reserva] e [Pedido Online]   em ranking de [melhor avaliação] e de [maior Preço para Dois]
         ou     Lista os Restaurantes [ Normal ou Cheap ]
         com [Entrega] e [Pedido Online]   em ranking de [melhor avaliação] e de [maior Preço para Dois]
    '''
    cols = [ 'restaurant', 'restaurant_name' ,'country_names', 'price_range', 'price_type', 'rating_category' , 'votes' , 'aggregate_rating' , 'average_cost_for_two' , 'is_delivering_now' , 'has_online_delivery', 'has_table_booking' ] 
    #
    df_aux = df1.loc[ : , cols ]
    df_aux['restaurant_name'] = df_aux['restaurant_name'].apply( lambda x: x.lower().title())
    df_aux['restaurant (country)'] = '- ' + df_aux['restaurant_name'] + ' (' + df_aux['country_names'] + ')'
    #
    # Filtrar  tiposCardapio
    dfa = pd.DataFrame(columns=[])
    for tpCard in tiposCardapio:
        dfb= df_aux.loc[ ( df_aux['price_type']==tpCard ) , : ].reset_index(drop=True)
        dfa = pd.concat([ dfa, dfb], ignore_index=True)
    df_aux = dfa.copy()
    #
    #
    # Filtrar  Reserva ou OnlineOrder
    # ''' Se for cardapio Gourmet,   procurar os que fazem reserva
    #     Se for cardapio Expensive, procurar os que fazem reserva e pedido online
    #     Se for cardapio Normal,    procurar os que fazem entrega e pedido online
    #     Se for cardapio Cheap,     procurar os que fazem entrega e pedido online
    # '''
    #
    if ('gourmet' in tiposCardapio):
        #print( 'Aqui ', tiposCardapio )
        df_aux = df_aux.loc[ df_aux['has_table_booking']==1 , : ].reset_index(drop=True)
        textSession = 'Lista os Restaurantes Gourmet que fazem Reserva'
    elif ('expensive' in tiposCardapio):
        #print( 'Aqui expensive' )
        df_aux = df_aux.loc[ ( ( df_aux['has_table_booking']==1 ) & ( df_aux['has_online_delivery']==1 ) ), : ].reset_index(drop=True)
        textSession = 'Lista os Restaurantes Expensive que fazem Pedido Online'
    else:
        #print( 'Aqui ', tiposCardapio )
        df_aux = df_aux.loc[ ( ( df_aux['is_delivering_now']==1 ) & ( df_aux['has_online_delivery']==1 ) ), : ].reset_index(drop=True)
        textSession = 'Lista os Restaurantes Expensive que fazem Pedido Online'
    #
    #st.dataframe( df_aux )
    #
    cols_grpby = [ 'restaurant (country)' , 'price_type' , ]
    df_aux = ( df_aux.groupby( cols_grpby )
                     .agg({ 'aggregate_rating': ['mean'],  'votes':['sum'],  'average_cost_for_two':['mean'] })
             )
    df_aux.columns = df_aux.columns.map(' '.join)
    df_aux = df_aux.reset_index()
    #
    df_aux.columns = [ 'Restaurante (País)', 'Tipo do Cardápio', 'Avaliação Média (scores de 0 a 5)', 'Total de Votos', 'Preço médio do Prato para dois' ]
    df_aux = df_aux.reset_index().sort_values( [ 'Avaliação Média (scores de 0 a 5)', 'Total de Votos', 'Preço médio do Prato para dois' ] , ascending=False).reset_index(inplace=False,drop=True).drop('index', axis=1)
    #
    df_aux['Avaliação Média (scores de 0 a 5)'] =  df_aux['Avaliação Média (scores de 0 a 5)'].round(2).astype(str)
    df_aux['Total de Votos'] = df_aux['Total de Votos'].round(2).astype(str)
    df_aux['Avaliação Média (Total de Votos)']  =  df_aux['Avaliação Média (scores de 0 a 5)'] + ' ('+df_aux['Total de Votos']+')'
    df_aux = df_aux.reset_index().sort_values( [ 'Avaliação Média (Total de Votos)', 'Preço médio do Prato para dois' ] , ascending=False).reset_index(inplace=False,drop=True).drop(['index'], axis=1)
    df_aux = df_aux[[ 'Restaurante (País)', 'Avaliação Média (Total de Votos)', 'Preço médio do Prato para dois' ]] # 'Tipo do Cardápio', 
    #
    #display( df_aux )   ####
    return df_aux
#
#
# --------------------------------- -------------------------------- ------------------------    Plot   Boxplot
def boxplotChart( df_aux, cols , y_axis_name , boxplot_width, boxplot_height ):
    ''' FUNÇÃO para plot de múltiplos boxplot
    '''
    #  'country_names'         cols[0]
    #  'average_cost_for_two'  cols[1]
    # Create layout with specified width and height
    layout = go.Layout(
        width  = boxplot_width,  # Set width to 800 pixels
        height = boxplot_height,  # Set height to 400 pixels
    )
    #
    fig = go.Figure( layout = layout )
    #
    colorsBox = [ 'indianred' , 'rgb(107,174,214)' , '#FF851B' , 'lightseagreen', '#FF80DF' , '#4dff4d' , '#ff66a3',
                  'indianred' , 'rgb(107,174,214)' , '#FF851B' , 'lightseagreen', '#FF80DF' , '#4dff4d' , '#ff66a3',
                  'indianred' , 'rgb(107,174,214)' , '#FF851B' , 'lightseagreen', '#FF80DF' , '#4dff4d' , '#ff66a3',
                  'indianred' , 'rgb(107,174,214)' , '#FF851B' , 'lightseagreen', '#FF80DF' , '#4dff4d' , '#ff66a3'
                ]
    #
    # takes each element of list   list(df_aux[cols[0]].unique())  and plots each boxplot
    for i,cnt in enumerate( list(df_aux[cols[0]].unique()) ):
        # print( i , '  ', type(i)  , ' color ')
        df_col1 = df_aux.loc[ df_aux[cols[0]]==cnt ,  cols[1] ]
        fig.add_trace( go.Box( y=df_col1 , name=cnt , marker_color = colorsBox[i] ) )
    #
    fig.update_traces(boxpoints='all', jitter=0)
    #
    #
    # =====================  Titles  =========================
    fig.update_layout(
        yaxis_title = y_axis_name,  # Set y-axis title
        xaxis_title = '',  # Exclude x-axis title
        title       = '',  # Exclude plot title
        font        = dict(size=10),  # Set font size to a very small value
        plot_bgcolor= 'white',  # Set plot background color
        margin      = dict(l=50, r=50, t=10, b=20),  # Set margins
        legend      = None, # dict(title='Legend', orientation='h', x=0.5, y=-0.2),  # Customize legend
        showlegend  = False,  # Do not display the legend
        hovermode   = 'closest',  # Set hover mode
        #boxmode='group'  # Group together boxes of different traces for each value of x
    )
    return fig
#
#
def show_bestrestaurants_ScoreVotes( pricetype_item, df_aux, backgcolr , tagShowHTML ):
    '''  FUNÇÃO Encontra os 5 restaurantes com seus países considerados melhores pelos maiores Avalição Média e Quantidade de Votos '''
    df_auxtmp = df_aux.loc[  df_aux['price_type']==pricetype_item, : ].reset_index(drop=True)
    df_auxtmp['restaurant (country)'] = '- ' + df_auxtmp['restaurant_name'] + ' (' + df_auxtmp['country_names'] + ')'
    df_auxtmp = df_auxtmp.loc[ 0:4, ['restaurant (country)','aggregate_rating mean','votes sum'] ]
    df_auxtmp.columns = ['Restaurante (País)','Avaliação Média','Qtd de Votos Média']
    df_auxtmp = df_auxtmp.reset_index(drop=True)
    #
    mean_avalc = df_auxtmp['Avaliação Média'].mean().round(2)
    sum_votos = np.round(df_auxtmp['Qtd de Votos Média'].sum(),2)
    list_rest = str(list(df_auxtmp['Restaurante (País)'])).replace('[','').replace(']','').replace('\'','').replace('\"','').replace(',','<br>')
    #
    html = f'<div> (<span style="font-size: 14px; font-weight: bold; text-align: center;">Avaliação média: {mean_avalc}; Média de Votos: {sum_votos}</span>) <br></div>'
    html += f'<div> <span style="font-size: 16px; text-align: left;">{list_rest}</span> </div>' 
    #
    st.markdown(
        f"""
        <div style="padding: 10px; background-color: {backgcolr}; height: 330px;">
            <div style="font-size: 18px; font-weight: bold; text-align: center; line-height:38px" > Cardápio {pricetype_item.capitalize()} <br></div>
            <div style="font-size: 13px; text-align: center;"> Avaliação: {mean_avalc} | Votos: {sum_votos}  <br> <br></div>
            <div style="font-size: 14px; text-align: left; line-height:2 "> {list_rest} </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    return df_auxtmp
#
#
def obterdfaux_parasunburst( df1 ):
    df_aux = ( df1.loc[ : , ['price_type','rating_category','restaurant','country_names','aggregate_rating'] ]
              .groupby( [ 'price_type','rating_category','country_names' ] )
              .agg( { 'restaurant': [ 'count' ], 'aggregate_rating':['mean'] } )
         )
    df_aux.columns = [ 'Quantidade Restaurantes','Avaliação Média' ]
    df_aux = df_aux.reset_index()
    df_aux.columns = [ 'Tipo Cardápio','Categoria Avaliação','Países','Quantidade Restaurantes','Avaliação Média' ]
    df_aux = df_aux.reset_index().replace(0.0, 0.01)
    return df_aux
#
def sunbplot_cardapiocategoriaaval( df_aux ):    
    fig1 = px.sunburst( df_aux,
                       path=[ 'Tipo Cardápio', 'Categoria Avaliação'],
                       values='Quantidade Restaurantes',
                       color='Avaliação Média',
                       color_continuous_scale='RdBu',
                       color_continuous_midpoint= np.average( df_aux['Avaliação Média']) )
    return fig1
#
def sunbplot_paisescategoriaaval( df_aux ):    
    fig2 = px.sunburst( df_aux,
                       path=[ 'Países', 'Categoria Avaliação'],
                       values='Quantidade Restaurantes',
                       color='Avaliação Média',
                       color_continuous_scale='RdBu',
                       color_continuous_midpoint= np.average( df_aux['Avaliação Média']) )
    return fig2
#
#
#
# -----------------------------------------------------------------------------------------------------------------------------------------------------
print( "\n================================\nUsuário acessou a página Restaurants" )
#
#
# # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #    INÍCIO DA ESTRUTURA LÓGICA DO CÓDIGO   # # #  # # #  # # #  # # #  # # #  # # #  # # #  # # #
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Carregar os dados da tabela
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
df  = pd.read_csv( 'dataset/zomato.csv' )
df1 = df.copy()
#print( '\n\n\nJustRead', list(df1) ,'\n\n' )
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Aviso do horário de execução do .py
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
print( 'Current time:', datetime.now().strftime('%Y-%m-%d %H:%M:%S') )
print( "Possui ", len( df ) , "linhas na base" )
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
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
print( "Após limpeza e ajustes, df possui ", len( df1 ) , "linhas na base" )
#
#print( 'colunas:\n', sorted( list( df1 )) )
#
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Layout de visão no StreamLit para dashboards
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# -------------------- -------------------- -------------------- --------------------  Headers
#
image_path = '🍱'
#
markdown_content = f"""
    <div style="display: flex; justify-content: space-between; background-color: rgba(255, 255, 128, .5);  align-items: center;">
        <div style="font-size: 38px; font-weight: bold; margin-left:  10px; "> {image_path} Restaurants </div>
        <div style="font-size: 24px; font-weight: bold; margin-right: 10px; "> Fome Zero </div>
    </div>
    """
#
st.write( markdown_content , unsafe_allow_html=True )
#
#
# -------------------- -------------------- -------------------- --------------------  Sidebar
image_path = 'comidas.jpg'
image = Image.open( image_path )
#st.sidebar.image( image, width=120 )
markdown_content = f'<h1 style="text-align: center;"><img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" style="width: 55px; margin-right: 20px;">   Fome Zero </h1>'
st.sidebar.markdown(  markdown_content,  unsafe_allow_html=True  )
#
# - - Filtros do sidebar
st.sidebar.markdown( '### Filtros' )
#
# ---------- Países
optList_Countries = sorted( list( df1['country_names'].unique() ))
selectedCountries = st.sidebar.multiselect(
    'Selecionar Países',
    optList_Countries,
    [ optList_Countries[0] , 'United Arab Emirates' , optList_Countries[-1] ] )
#
# ---------- Culinária
st.sidebar.markdown( """---""" )
boolFilt_Cuisines = st.sidebar.toggle('Filtrar Tipo de Culinária')
optList_Cuisines = sorted( list( df1['cuisines'].unique() ))
if boolFilt_Cuisines:
    selectedCuisines = st.sidebar.multiselect(
        'Selecionar Tipo de Culinária',
        optList_Cuisines,
        [ optList_Cuisines[0] , 'Brazilian' , 'Japanese' ] )
else:
    selectedCuisines = optList_Cuisines
#
# st.sidebar.markdown( """---""" )                           #  - -  - -  - -  - - Fechamento do sidebar
# st.sidebar.markdown( 'Powered by CDS - Raíssa Thibes' )
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Aplicação de Filtro
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Backup sem filtro
dfarc = df1.copy()
#
linhas_selecionadas_Countries = df1['country_names'].isin( selectedCountries )
df1 = df1.loc[ linhas_selecionadas_Countries , : ]
linhas_selecionadas_Cuisines = df1['cuisines'].isin( selectedCuisines )
df1 = df1.loc[ linhas_selecionadas_Cuisines , : ]
#
print( "Sem filtros possui ", len( dfarc ) , "linhas na base\n" )
print( "Após aplicar filtros possui ", len( df1 ) , "linhas na base\n" )
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Visualizações das análises
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
#
st.markdown( """---""" )
#
with st.container():
    #
    markdown_content = f'<h3 style="text-align: center;"> Melhores Restaurantes </h3>'
    markdown_content += f'<p style="text-align: center;"> Veja abaixo os restaurantes com melhores avaliações médias e total de votos <br> separados por categoria de cardápio <br> </p>'
    st.markdown(  markdown_content,  unsafe_allow_html=True  )
    #
    #
    cols = [ 'restaurant', 'restaurant_name' ,'country_names', 'price_range', 'price_type', 'rating_category' , 'votes' , 'aggregate_rating' , 'average_cost_for_two' , 'booking', 
             'delivery',  'online_order' ]   # (df1['price_type']=='gourmet') & 
    df_aux = df1.loc[ (  (df1['rating_category']=='Excelente') ) , cols ].sort_values( ['aggregate_rating', 'votes'] , ascending=False)
    df_aux['restaurant_name'] = df_aux['restaurant_name'].apply( lambda x: x.lower().title())
    cols_grpby = [ 'restaurant_name' ,'country_names', 'price_range', 'price_type' ]
    df_aux = ( df_aux.groupby( cols_grpby )
                     .agg({'aggregate_rating': ['mean'], 'votes':['sum']})
             )
    df_aux.columns = df_aux.columns.map(' '.join)
    df_aux = df_aux.reset_index().sort_values( [ 'price_range' , 'price_type' , 'aggregate_rating mean', 'votes sum' ] , ascending=False).drop('price_range', axis=1).reset_index(drop=True)
    #
    pricetype = list( df_aux['price_type'].unique() )
    #
    #
    col1, col2, col3, col4 = st.columns( 4 )
    #
    with col1:
        # 'Melhores Restaurantes Gourmet'
        pricetype_item = pricetype[0]
        backgcolr = '#b3ffe6'
        dfaux_pricetype0 = show_bestrestaurants_ScoreVotes( pricetype_item, df_aux, backgcolr , tagShowHTML=True )
        #
    with col2:  
        # 'Melhores Restaurantes Expensive'
        pricetype_item = pricetype[1]
        backgcolr = '#00e6e6'
        dfaux_pricetype1 = show_bestrestaurants_ScoreVotes( pricetype_item, df_aux, backgcolr , tagShowHTML=True )
        #
    with col3:
        # 'Melhores Restaurantes Normal'
        pricetype_item = pricetype[2]
        backgcolr = '#b3ffe6'
        dfaux_pricetype2 = show_bestrestaurants_ScoreVotes( pricetype_item, df_aux, backgcolr , tagShowHTML=True )
        #
    with col4:
        # 'Melhores Restaurantes Cheap'
        pricetype_item = pricetype[3]
        backgcolr = '#00e6e6'
        dfaux_pricetype3 = show_bestrestaurants_ScoreVotes( pricetype_item, df_aux, backgcolr , tagShowHTML=True )
        #
#
with st.container():
    st.markdown( """---""" )
    markdown_content = f'<h3 style="text-align: center;"> Quantidade de Restaurantes <br>  <br> </h3>'
    st.markdown(  markdown_content,  unsafe_allow_html=True  )
    #
    df_aux = obterdfaux_parasunburst( df1 )
    #
    col1, col2 = st.columns( 2 )
    with col1:
        markdown_content = f'<h5 style="text-align: center;"> Tipo de Cardápio e Categoria de Avaliação Média </h5>'
        st.markdown( markdown_content,  unsafe_allow_html=True )
        fig1 = sunbplot_cardapiocategoriaaval( df_aux )
        st.plotly_chart( fig1 , use_container_width=True )
    with col2:
        markdown_content = f'<h5 style="text-align: center;"> País e Categoria de Avaliação Média </h5>'
        st.markdown( markdown_content,  unsafe_allow_html=True )
        fig2 = sunbplot_paisescategoriaaval( df_aux )
        st.plotly_chart( fig2 , use_container_width=True )
#
with st.container():
    st.markdown( """---""" )
    markdown_content = f'<h3 style="text-align: center;"> Relação de Restaurantes </h3>'
    markdown_content += f'<h5 style="text-align: center;"> Separados por categoria de cardápio <br> </h5>'
    st.markdown(  markdown_content,  unsafe_allow_html=True  )
    #
    df_final = pd.DataFrame(columns=[])
    #
    with st.container():
        #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  Gourmet cardápio
        st.markdown( " " )
        tiposCardapio = [ 'Gourmet' ]
        textSession = 'Cardápio Gourmet com Reserva'
        #
        df_aux = show_bestrestaurants_listaGourmetExpensive( tiposCardapio , df1 )
        df_final = pd.concat([df_final, df_aux], ignore_index=True)
        #
        with st.expander( textSession ):
            if len(df_aux)>0:
                st.dataframe( df_aux.set_index(df_aux.columns[0]) , use_container_width=True  )
            else:
                markdown_content = f'<p style="text-align: center;"> Nenhum restaurante foi encontrado para as seleções dos filtros ao lado </p>'
                st.markdown(  markdown_content,  unsafe_allow_html=True  )
    #
    with st.container():
        #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  Expensive cardápio
        st.markdown( " " )#; st.markdown( "Expensive" )
        tiposCardapio = [ 'Expensive' ]
        textSession = 'Cardápio Expensive com Reserva e Pedido Online'
        #
        df_aux = show_bestrestaurants_listaGourmetExpensive( tiposCardapio , df1 )
        df_final = pd.concat([df_final, df_aux], ignore_index=True)
        #
        with st.expander( textSession ):
            if len(df_aux)>0:
                st.dataframe( df_aux.set_index(df_aux.columns[0]) , use_container_width=True  )
            else:
                markdown_content = f'<p style="text-align: center;"> Nenhum restaurante foi encontrado para as seleções dos filtros ao lado </p>'
                st.markdown(  markdown_content,  unsafe_allow_html=True  )
    #
    with st.container():
        #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  Normal cardápio
        st.markdown( " " )#; st.markdown( "Normal" )
        tiposCardapio = [ 'Normal' ]
        textSession = 'Cardápio Normal com Entrega e Pedido Online'
        #
        df_aux = show_bestrestaurants_listaGourmetExpensive( tiposCardapio , df1 )
        df_final = pd.concat([df_final, df_aux], ignore_index=True)
        #
        with st.expander( textSession ):
            if len(df_aux)>0:
                st.dataframe( df_aux.set_index(df_aux.columns[0]) , use_container_width=True  )
            else:
                markdown_content = f'<p style="text-align: center;"> Nenhum restaurante foi encontrado para as seleções dos filtros ao lado </p>'
                st.markdown(  markdown_content,  unsafe_allow_html=True  )
                
    #
    with st.container():
        #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  Cheap cardápio
        st.markdown( " " )#; st.markdown( "Cheap" )
        tiposCardapio = [ 'Cheap' ]
        textSession = 'Cardápio Cheap com Entrega e Pedido Online'
        #
        df_aux = show_bestrestaurants_listaGourmetExpensive( tiposCardapio , df1 )
        df_final = pd.concat([df_final, df_aux], ignore_index=True)
        #
        with st.expander( textSession ):
            if len(df_aux)>0:
                st.dataframe( df_aux.set_index(df_aux.columns[0]) , use_container_width=True  )
            else:
                markdown_content = f'<p style="text-align: center;"> Nenhum restaurante foi encontrado para as seleções dos filtros ao lado </p>'
                st.markdown(  markdown_content,  unsafe_allow_html=True  )
#
