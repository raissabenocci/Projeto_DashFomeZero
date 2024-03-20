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
def findCuisine1( df_def, cols, strMid, strMetric, colorBkg, booldropduplicate ):
    '''  FUNÇÂO  para achar cuisines baseado em qual coluna
    '''
    df_aux =  df_def.loc[ : , cols]
    if booldropduplicate:
        df_aux = df_aux.drop_duplicates()
        df_aux = df_aux.reset_index()
    else:
        df_aux = df_aux.copy() 
    df_aux = df_aux.groupby( [ cols[0] ] ).agg( {cols[-1]: strMetric} )
    df_aux = df_aux.reset_index()
    #display( df_aux )
    maxValue   = df_aux[ cols[-1] ].max()
    strCuls    = df_aux.loc[ df_aux[ cols[-1] ]==maxValue , cols[0] ].values
    Cul_maxValue = str( strCuls ).replace('[','').replace(']','').replace('\'','').replace(',','<br>')
    singplu    = 's' if len(strCuls)>1 else ''
    #
    st.markdown(
        f"""
        <div style="padding: 10px; background-color: {colorBkg}; text-align: center; height: 180px;">
            <div style="font-size: 15px; font-weight: bold;"> Culinária{singplu} {strMid} ({maxValue}) <br> <br> </div>
            <div style="font-size: 18px; "> {Cul_maxValue}  <br> </div>
        </div>
        """,
        unsafe_allow_html=True
    )
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
#
# -----------------------------------------------------------------------------------------------------------------------------------------------------
print( "\n================================\nUsuário acessou a página Cuisines" )
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
image_path = '🧑‍🍳'

markdown_content = f"""
    <div style="display: flex; justify-content: space-between; background-color: rgba(255, 255, 128, .5);  align-items: center;">
        <div style="font-size: 38px; font-weight: bold; margin-left:  10px; "> {image_path} Cuisines </div>
        <div style="font-size: 24px; font-weight: bold; margin-right: 10px; "> Fome Zero </div>
    </div>
    """
st.markdown( markdown_content , unsafe_allow_html=True )
#
#
# -------------------- -------------------- -------------------- --------------------  Sidebar
image_path = 'comidas.jpg'
image = Image.open( image_path )
#st.sidebar.image( image, width=120 )
image_base64 = base64.b64encode(open(image_path,"rb").read()).decode()
markdown_content = f'<h1 style="text-align: center;">  <img src="data:image/png;base64,{image_base64}" style="width: 55px; margin-right: 20px;">   Fome Zero </h1>'
st.sidebar.markdown(  markdown_content  ,  unsafe_allow_html=True  )
#
# - - Filtros do sidebar
st.sidebar.markdown( '### Filtros' )
#
#
# ---------------------- Categoria de Preço
optList_PriceType = sorted( list( df1['price_type'].unique() ))
selectedPriceType = st.sidebar.multiselect(
    'Escolha a categoria de preço',
    optList_PriceType,
    optList_PriceType )
if len(selectedPriceType)<0:
    selectedPriceType = ['Cheap']
#
#
# ---------------------- Países
optList_Countries = sorted( list( df1['country_names'].unique() ))
filtCntr = st.sidebar.checkbox('Filtrar Países também')
if filtCntr:
    selectedCountries = st.sidebar.multiselect(
        'Selecionar Países',
        optList_Countries,
        [ optList_Countries[0] , 'United Arab Emirates' , optList_Countries[-1] ] )
else:
    selectedCountries = optList_Countries
#
# ---------------------- Retirar Outliers ?
# st.sidebar.markdown( "Retirar outliers do Preço médio para dois?" )
# offOutlier  = st.sidebar.checkbox( 'Sim' ,   value=True )
# #
# st.sidebar.markdown( """---""" )                           #  - -  - -  - -  - - Fechamento do sidebar
# st.sidebar.markdown( 'Powered by CDS - Raíssa Thibes' )
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Aplicação de Filtro
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Backup sem filtro
dfarc = df1.copy()
#
linhas_selecionadas = df1['price_type'].isin( selectedPriceType )
df1 = df1.loc[ linhas_selecionadas, : ]
df1_pryTp = df1.copy()
if filtCntr:
    linhas_selecionadas_Countries = df1['country_names'].isin( selectedCountries )
    df1 = df1.loc[ linhas_selecionadas_Countries , : ]
#
print( "Sem filtros possui " ,          len( dfarc ) , "linhas na base\n" )
print( "Após aplicar filtros possui " , len(  df1  ) , "linhas na base\n" )
#
#
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#  Visualizações das análises
# ---------------------------------------------------------------------------------------------------------------------------------------------------
#
st.markdown( """---""" )
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Tipos de Culinária : quantidade
# Create grouped bar chart using Plotly Express
# Qtd tipos de culinária
with st.container():
    markdown_content = f'<h2 style="text-align: center;"> Tipos de Culinárias métricas mais elevadas <br> <br> </h2>'
    st.markdown(  markdown_content,  unsafe_allow_html=True  )
    #
    considerAll = True
    df_def = dfarc.copy() if considerAll else df1.copy()
    #
    #st.dataframe( df_def.loc[ : , [ 'restaurant' , 'country_names' , 'cuisines' , 'aggregate_rating' , 'is_delivering_now' , 'price_range' , 'price_type' ] ] )
    #
    #
    col1, col2, col3, col4, col5, col6 = st.columns( [1,1,1,1,1,2] )
    #
    with col1:    # - - - - - - - - - - - - - - - - - - - - -   Total de Culinárias
        amountCsn = len( dfarc['cuisines'].unique() )
            #
        # se st.markdown() to apply the background color to a container
        st.markdown(
            f"""
            <div style="padding: 10px; background-color: {'#00e6e6'}; text-align: center; height: 180px;">
                <div style="font-size: 16px; font-weight: bold; line-height: 200%; "> Total <br> Culinárias <br> </div>
                <div style="font-size: 18px; align-items: center; line-height: 350%; "> <span style="font-size: 30px; "> {amountCsn} </span> </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:    # - - - - - - - - - - - - - - - - - - - - -   Culinária(s) com mais restaurantes
        # Rest
        cols = [ 'cuisines' , 'restaurant' ]
        strMid = 'em <br> mais restaurantes <br> '
        strMetric = 'count'
        findCuisine1( df_def, cols, strMid, strMetric, colorBkg='#b3ffe6', booldropduplicate=False )
        #
    with col3:    # - - - - - - - - - - - - - - - - - - - - -   Culinária(s) em mais países
        # Countries
        cols = [ 'cuisines' , 'country_names' ]
        strMid = 'em <br> mais países <br> '
        strMetric = 'count'
        findCuisine1( df_def, cols, strMid, strMetric, colorBkg='#00e6e6', booldropduplicate=True )
        #
    with col4:    # - - - - - - - - - - - - - - - - - - - - -   Culinária(s) com melhor avaliação
        # Avaliação
        cols = [ 'cuisines' , 'aggregate_rating' ]
        stringMid = 'com <br> maior avaliação <br> '
        strMetric = 'mean'
        findCuisine1( df_def, cols, stringMid, strMetric, colorBkg='#b3ffe6', booldropduplicate=False )
        #
    with col5:    # - - - - - - - - - - - - - - - - - - - - -   Culinária(s) com mais entregas
        # Delivery
        cols = [ 'cuisines' , 'is_delivering_now' ]
        strMid = 'com <br> mais entregas <br> '
        strMetric = 'sum'
        findCuisine1( df_def, cols, strMid, strMetric, colorBkg='#00e6e6', booldropduplicate=False )
        #
    with col6:    # - - - - - - - - - - - - - - - - - - - - -   Culinária(s) com melhor avaliação
        # Dataframe de correspondência entre Price Range e Price Type
        dfprice = df1.loc[:,['price_range','price_type']].drop_duplicates().sort_values( ['price_range'] , ascending=False ).reset_index(inplace=False, drop=True)
        #
        # Inicializar variável html
        html = f''
        #
        for _,row_price in dfprice.iterrows():
            cols = [ 'cuisines' , 'price_range' ]
            df_aux = df1.loc[ df_def[cols[1]]==row_price['price_range'] , cols ] #
            df_aux = df_aux.groupby('cuisines').count()
            df_aux = df_aux.reset_index()
            df_aux = df_aux.sort_values( list(df_aux)[1] , ascending=False )
            #st.dataframe( df_aux )
            #
            strPrcTyp        = row_price['price_type'].capitalize() 
            maxCount         = df_aux.iloc[0,1]
            Cuisine_maxCount = df_aux.iloc[0,0]
            #
            htinfo = f'<span style="font-weight: bold; text-align: justify;">  - {strPrcTyp} </span> (<span style="font-weight: bold;">{maxCount}</span>): {Cuisine_maxCount}'
            html += f'<div style="text-align: justify; line-height: 2"> {htinfo} </div>'
            #
        #
        st.markdown(
            f"""
            <div style="padding: 10px; background-color: {'#b3ffe6'}; text-align: center; height: 180px;">
                <div style="font-weight: bold; line-height: 2"> Culinárias por tipo de cardápio </div>
                {html}
            </div>
            """,
            unsafe_allow_html=True
        )
#
# Create grouped bar chart using Plotly Express
# Qtd tipos de culinária
with st.container():
    #
    st.markdown( """---""" )
    #
    cols = [ 'cuisines' , 'restaurant' ]
    df_aux = ( df1
               .loc[ : , cols]
               .groupby( [ 'cuisines' ] ).count()
             )
    df_aux = df_aux.reset_index()
    df_aux.columns = [ 'Culinárias' , 'Quantidades de Restaurantes' ]
    df_aux_bkup = df_aux.copy()
    #
    with st.container():
        col1, col2 = st.columns( [ 1, 4] , gap="medium" )
        with col1:
            with st.container():
                st.markdown( '<h6 style="text-align: justify;"> O que deseja ver? </h6>' , unsafe_allow_html=True)
                topBottom = st.radio(
                                      "",
                                      [":rainbow[Top] ✅", "***Bottom*** ⚠️" ],
                                      captions = ["Mais Restaurantes", "Menos Restaurantes" ]
                                    )
                #
                if topBottom == ":rainbow[Top] ✅":
                    topBottom = 'Top'
                    maisMenos = 'mais'
                    df_aux = df_aux.sort_values( ['Quantidades de Restaurantes'] , ascending=False)
                    amtDeft = 10
                elif topBottom == "***Bottom*** ⚠️":
                    topBottom = 'Bottom'
                    maisMenos = 'menos'
                    df_aux = df_aux.sort_values( ['Quantidades de Restaurantes'] , ascending=True)
                    amtDeft = 20
                df_aux = df_aux.reset_index(inplace=False, drop=True)
            #
            with st.container():
                st.markdown( " " )
                st.markdown( '<h6 style="text-align: justify;"> <br> <br> Quantas culinárias? </h6>' , unsafe_allow_html=True)
                #amount = st.slider( '' , 0 , len(df_aux [ 'Culinárias' ]) , amtDeft )
                amount = st.select_slider( '' ,   options=[5, 10, 15, 20, 25, 30] , value=amtDeft )
                #st.markdown( "amount " + str(amount) )
        with col2:
            with st.container():               # # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -   Top Culinárias  com mais restaurantes
                markdown_content = f'<h3 style="text-align: center;"> {topBottom} {amount} Culinárias <br> </h3>'
                markdown_content += f'<h4 style="text-align: center;">  com {maisMenos} Restaurantes <br> </h4>'
                st.markdown(  markdown_content,  unsafe_allow_html=True  )
                #
                df_auxTopBottom = df_aux.iloc[0:(amount), : ]
                #
                # Create grouped bar chart using Plotly Express
                fig_px = px.bar(df_auxTopBottom, x='Culinárias', y='Quantidades de Restaurantes',
                                labels={'Quantidades de Restaurantes': 'Quantidade de Restaurantes'},
                                category_orders={'Culinárias': sorted(df_auxTopBottom['Culinárias'].unique())},
                                text='Quantidades de Restaurantes')  # Specify the text to be displayed on each bar
                #
                # Update layout of the figure
                fig_px.update_layout(
                    width=600,  # Set width to 600 pixels
                    height=500,  # Set height to 500 pixels
                    xaxis_tickangle=-45  # Rotate x-axis labels by 45 degrees
                )
                #
                # Convert Plotly Express figure to graph object figure
                fig_go = go.Figure( fig_px )
                #
                # Update layout of the figure
                fig_go.update_layout(
                    # title='Grouped Bar Chart of Three Categorical Variables',
                    # xaxis_title='Category2',
                    # yaxis_title='Category1',
                    width=600,  # Set width to 800 pixels
                    height=500,  # Set height to 600 pixels
                    margin      = dict(l=50, r=50, t=10, b=20),  # Set margins
                    xaxis={'tickangle': -90}  # Rotate x-axis labels by -45 degrees
                )
                #
                # st.dataframe( df_auxTop  , use_container_width=True )
                st.plotly_chart( fig_go , use_container_width=True )
    #
#
st.markdown( """---""" )
#
with st.container():  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Tipos de Culinária 
    markdown_content = f'<h3 style="text-align: center;"> Tipos de culinária <br> </h3>'
    st.markdown(  markdown_content,  unsafe_allow_html=True  )
    #
    st.markdown( "##### Selecione abaixo para ver detalhes" )
    #
    with st.container():   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Selecionar Culinárias
        #
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Filtro
        #    Definir 3 principais culinárias, pela maior quantidade de restaurantes
        df_aux2 = df1.loc[ : , [ 'restaurant' , 'cuisines'  ] ].groupby( 'cuisines' ).count().reset_index().sort_values( [ 'restaurant' ] , ascending=False ).reset_index()
        initCuis = [df_aux2.loc[0,'cuisines'],df_aux2.loc[1,'cuisines'],df_aux2.loc[2,'cuisines']]
        #
        #    Selecionar tipos de culinárias, usando a initCuis como Culinárias já pré-selecionadas
        selectedCuisines = st.multiselect(
            'Culinárias',
            sorted( list( df1['cuisines'].unique() )),
            initCuis)
        #
        #     Aplicação de Filtro
        linhas_selecionadas_Cuisines = df1['cuisines'].isin( selectedCuisines )
        df_aux = df1.loc[ linhas_selecionadas_Cuisines , [ 'cuisines' , 'restaurant_name' , 'price_type' , 'country_names' , 'online_order', 'booking', 'delivery', 'restaurant' ] ]
        #
        #
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Agrupar para st.dataframe
        #  Qtd tipos de culinária
        cols = [ 'restaurant' , 'cuisines' , 'restaurant_name' , 'price_type' ]
        df_aux = df_aux.loc[ : , cols].groupby( [ 'cuisines' , 'price_type' , 'restaurant_name' ] ).count().reset_index()
        df_aux.columns = [ 'Culinárias' , 'Categorias' , 'Restaurantes' , 'Quantidades de Restaurantes' ]
        df_aux = df_aux.sort_values( [ 'Culinárias' , 'Categorias' , 'Restaurantes' ] ).reset_index(drop=True)
        df_aux22 = df_aux.copy()
        #st.dataframe( df_aux.set_index(df_aux.columns[0]) , use_container_width=True  )
        #
        #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Definir se visível  st.dataframe
        #
        varVisbl = st.checkbox( "Mostrar tabela das Culinárias, com Categoria de cardápio e Restaurantes" , key="disabled")
        if varVisbl:
            col_info1, col_info2 = st.columns( 2, gap="medium" )
            with col_info1:
                df_aux_info1 = df_aux.loc[ : , ['Culinárias' , 'Categorias' , 'Quantidades de Restaurantes']].groupby( ['Culinárias' , 'Categorias' ] ).sum().reset_index()
                st.write( "Quantidade de Restaurantes por Culinária e Categoria do cardápio" )
                st.dataframe( df_aux_info1.set_index(df_aux_info1.columns[0]) , use_container_width=True  )
                #
            with col_info2:
                df_aux_info2 = df_aux22.loc[:, ['Culinárias' , 'Categorias' , 'Restaurantes'] ].drop_duplicates().reset_index(inplace=False,drop=True)
                st.write( "Lista de Restaurantes" )
                st.dataframe( df_aux_info2.set_index(df_aux_info2.columns[0]) , use_container_width=True  )
            #
        #
        #
    with st.container(): # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -   Agrupar para barplot de  Reserva  Delivery e Pedidos Online
        st.markdown( " " )
        markdown_content = f'<h4 style="text-align: center;"> <br> Reserva, Delivery e Pedidos Online </h4>'
        st.markdown(  markdown_content,  unsafe_allow_html=True  )
        #
        cols = [ 'cuisines' , 'restaurant' ,     'online_order', 'booking', 'delivery' ]
        filt_forBarplot = linhas_selecionadas_Cuisines
        df_aux = df1.loc[ filt_forBarplot , cols ]
        df_aux = df_aux.groupby( [ 'cuisines' , 'online_order', 'booking', 'delivery' ]).count()
        df_aux = df_aux.reset_index()
        df_aux.columns = [ 'Culinárias' , 'Pedir' , 'Reserva' , 'Delivery' , 'Quantidade' ]
        #
        #
        col1, col2 = st.columns( [2,5] )
        with col1:
            # Retirar linhas de Pedir Pessoalmente
            on = st.toggle('Considerar apenas os pedidos online')
        with col2:
            if on:
                df_aux = df_aux.loc[ df_aux['Pedir'] != 'Pessoalmente' , :]
                markdown_content = f'<p style="text-align: center;">  </p>'
            else:
                markdown_content = f'<p style="text-align: left;"> Observação: Dentro de um plot, os gráficos da esquerda referem-se a Pedir Online e da direita, a Pedir Pessoalmente </p>'
            st.markdown(  markdown_content,  unsafe_allow_html=True  )
        #
        # Create grouped bar chart using Plotly Express
        fig_px = px.bar( df_aux , x='Pedir', y='Quantidade', color='Reserva', barmode="group", facet_col='Delivery', facet_row="Culinárias",
                     category_orders={ 'Pedir':    ['Online', 'Pessoalmente'],
                                       'Reserva':  ['Reserva', 'Imediata'],
                                       'Delivery': ['Sem entrega', 'Entrega'] })
        #
        # Convert Plotly Express figure to graph object figure
        fig_go = go.Figure( fig_px )
        #
        # Update layout of the figure
        fig_go.update_layout(
            # title='Grouped Bar Chart of Three Categorical Variables',
            # xaxis_title='Category2',
            yaxis_title='',
            width=600,  # Set width to 800 pixels
            height=len(df_aux['Culinárias'].unique())*270  # Set height to amount of Countries times 270 pixels
        )
        #
        st.plotly_chart( fig_go , use_container_width=True )
#