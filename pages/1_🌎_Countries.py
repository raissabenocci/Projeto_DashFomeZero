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
print( "\n================================\nUsuário acessou a página Countries" )
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
# ----------------------------------------- -------------------- --------------------  Headers
# st.markdown( "#### Fome Zero!" )
image_path = '🌎'
#
markdown_content = f"""
    <div style="display: flex; justify-content: space-between; background-color: rgba(255, 255, 128, .5);  align-items: center;">
        <div style="font-size: 38px; font-weight: bold; margin-left:  10px; "> {image_path} Countries </div>
        <div style="font-size: 24px; font-weight: bold; margin-right: 10px; "> Fome Zero </div>
    </div>
    """
#
st.write( markdown_content , unsafe_allow_html=True )
# #
# header = st.container()
# header.title( '🌎 Countries' )
# header.write( """<div class='fixed-header'/>""" , unsafe_allow_html=True)
# #
# ### Custom CSS for the sticky header
# st.markdown(
#     """
# <style>
#     div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
#         top: 2.875rem;
#         background-color: rgba(255, 255, 128, .5);
#         z-index: 999;
#     }
# </style>
#     """,
#     unsafe_allow_html=True
# )
# position: sticky;
#
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
# ---------- Categoria de Preço
optList_PriceType = sorted( list( df1['price_type'].unique() ))
selectedPriceType = st.sidebar.multiselect(
    'Escolha a categoria de preço',
    optList_PriceType,
    optList_PriceType )
if len(selectedPriceType)<0:
    selectedPriceType = ['Cheap']
#
# ---------- Retirar Outliers ?
st.sidebar.markdown( "Retirar outliers do Preço médio para dois?" )
offOutlier  = st.sidebar.checkbox( 'Sim' ,   value=True )
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
linhas_selecionadas = df1['price_type'].isin( selectedPriceType )
df1 = df1.loc[ linhas_selecionadas, : ]
df1_pryTp = df1.copy()
linhas_selecionadas_Countries = df1['country_names'].isin( selectedCountries )
df1 = df1.loc[ linhas_selecionadas_Countries , : ]
#
print( "Sem filtros possui ", len( dfarc ) , "linhas na base\n" )
print( "Após aplicar filtros possui ", len( df1 ) , "linhas na base\n" )
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =  
#  Visualizações das análises
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Qtd Restaurantes
with st.container():
    st.markdown( """---""" )
    markdown_content = f'<h3 style="text-align: center;"> Quantidade de restaurantes cadastrados & Avaliação média <br> <br> </h3>'
    st.markdown(  markdown_content,  unsafe_allow_html=True  )
    #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Função para agrupar
    def countByCountry( df1, cols, renameCol, metricType ):
        df_aux = df1.loc[ : , cols]
        df_aux = df_aux.drop_duplicates()                                  # Excluir duplicatas
        df_aux = df_aux.reset_index( inplace=False, drop=True)
        #
        if metricType=='count':
            df_aux = df_aux.groupby( [ 'country_names' ] ).count()         # Agrupar por país contando
        elif  metricType=='sum':
            df_aux = df_aux.groupby( [ 'country_names' ] ).sum()          # Agrupar por país somando
        elif  metricType=='mean':
            df_aux = df_aux.groupby( [ 'country_names' ] ).mean()          # Agrupar por país usando média
        df_aux = df_aux.reset_index()
        df_aux.columns = [ 'País', renameCol ]                             # Renomear colunas
        df_aux = df_aux.sort_values( ['País'] , ascending=True )           # Reordenar pela quantidade de restaurantes
        df_aux = df_aux.reset_index( inplace=False, drop=True )
        return df_aux
    #
    cols = [ 'country_names' , 'restaurant' ]
    renameCol = 'Quantidade de Restaurantes'
    metricType = 'count'
    df_aux1 = countByCountry( df1_pryTp, cols, renameCol, metricType )
    #
    cols = [ 'country_names' , 'aggregate_rating' ]
    renameCol = 'Avaliação Média (limites: 0 a 5)'
    metricType = 'mean'
    df_aux2 = countByCountry( df1_pryTp, cols, renameCol, metricType )
    #
    cols = [ 'country_names' , 'votes' ]
    renameCol = 'Total de Votos'
    metricType = 'sum'
    df_aux3 = countByCountry( df1_pryTp, cols, renameCol, metricType )
    #
    #
    # # Perform left join
    left_join_df = pd.merge( pd.merge(df_aux1,df_aux2,on='País', how='left'), df_aux3, on='País', how='left')    # merge para left join usando País como chave
    left_join_df = left_join_df.sort_values( ['País'] , ascending=True )   # Reordenar pela quantidade de restaurantes
    left_join_df = left_join_df.reset_index( inplace=False, drop=True )
    left_join_df['Avaliação Média (limites: 0 a 5)'] = left_join_df['Avaliação Média (limites: 0 a 5)'].round(2)
    print( left_join_df )
    #
    # # Show dataframe
    st.dataframe(  left_join_df.style.format({'Avaliação Média (limites: 0 a 5)': '{:.2f}'}).highlight_max( axis=0, color='darkseagreen') ,
                   hide_index=True, use_container_width=True , height=len(left_join_df) * 37 
                )
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Tipos de Culinária , Restaurantes, Categoria de Preço
st.markdown( """---""" )
st.markdown( "### Selecione abaixo para ver detalhes" )
#
tab1, tab2, tab3 = st.tabs( ['Culinárias', 'Contagens: Reservas, Delivery, Pedido_Online', 'Distribuição de Preços' ] )
#
with tab1: 
    with st.container():  # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Tipos de Culinária 
        markdown_content = f'<h3 style="text-align: center;"> Tipos de culinária <br> </h3>'
        st.markdown(  markdown_content,  unsafe_allow_html=True  )
        #
        #  Qtd tipos de culinária
        cols = [ 'country_names' , 'cuisines' , 'restaurant' ]
        df_aux = ( df1.loc[ : , cols]
                  .groupby( [ 'country_names' , 'cuisines' ] ).count()
                 )
        df_aux = df_aux.reset_index()
        df_aux.columns = [ 'Países' , 'Culinárias' , 'Quantidade' ]
        df_aux = df_aux.sort_values( [ 'Culinárias' ] )
        #st.dataframe( df_aux )
        #
        # Create grouped bar chart using Plotly Express
        fig_px = px.bar( df_aux, x='Culinárias', y='Quantidade', color='Países',
                         labels={'Quantidade de Restaurantes':'Quantidade'}, 
                         category_orders={'Culinárias': sorted( df_aux['Culinárias'].unique() ) }
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
            height=690,  # Set height to 600 pixels
            margin      = dict(l=50, r=50, t=10, b=20),  # Set margins
            xaxis={'tickangle': -90}  # Rotate x-axis labels by -45 degrees
        )
        #
        st.plotly_chart( fig_go , use_container_width=True )
    #
with tab2:
    with st.container():   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Cont Reserva Delivery e Pedidos Online
        markdown_content = f'<h3 style="text-align: center;"> Contagens de Reserva, Delivery e Pedidos Online </h3>'
        st.markdown(  markdown_content,  unsafe_allow_html=True  )
        #
        cols = [ 'country_names' , 'restaurant' ,
                 'online_order', 'booking', 'delivery'
               ]
        df_aux = df1.loc[ : , cols ]
        df_aux = df_aux = df_aux.groupby( [ 'country_names' , 'online_order', 'booking', 'delivery' ]).count()
        df_aux = df_aux.reset_index()
        df_aux.columns = [ 'País' , 'Pedir' , 'Reserva' , 'Delivery' , 'Quantidade' ]
        # display( df_aux )
        #
        # Create grouped bar chart using Plotly Express
        fig_px = px.bar( df_aux , x='Pedir', y='Quantidade', color='Reserva', barmode="group", facet_col='Delivery',
                     category_orders={'Pedir': ['Online', 'Pessoalmente'],
                                      'Reserva':       ['Reserva', 'Imediata'],  
                                      'Delivery':      ['Entrega', 'Sem entrega']})
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
            height=500  # Set height to 600 pixels
        )
        #
        st.plotly_chart( fig_go , use_container_width=True )
    #
with tab3:
    with st.container():      # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Dist Preços
        markdown_content = f'<h3 style="text-align: center;"> Distribuição dos Preços do Prato para dois </h3>'
        st.markdown(  markdown_content,  unsafe_allow_html=True  )
        #
        df_aux = df1.copy()
        #
        col1, col2 = st.columns( [3, 1])
        #
        if  len(df_aux)>0:
            # Se sim para retirar outliers
            if offOutlier:
                # Calculate quartiles and IQR
                Q1 = df_aux['average_cost_for_two'].quantile(0.15)
                Q3 = df_aux['average_cost_for_two'].quantile(0.95)
                IQR = Q3 - Q1
                #
                # Define lower and upper bounds for outliers
                lower_bound = Q1 - 2.5 * IQR
                upper_bound = Q3 + 2.5 * IQR
                #
                # Identify outliers
                outliers = df1[ (df_aux['average_cost_for_two'] <  lower_bound) | (df1['average_cost_for_two'] > upper_bound) ]
                outliers = outliers.drop_duplicates().sort_values( ['average_cost_for_two'] , ascending=False)
                outliers = outliers.reset_index( inplace=False , drop=True )
                outliers = outliers.loc[:,['country_names','average_cost_for_two','currency','cuisines']]
                outliers.columns = ['País','Preço médio para 2','Moeda','Tipo de culinária']
                #
                # O que sobrou no dataframe df_aux
                df_aux   = df_aux[ (df_aux['average_cost_for_two'] <= upper_bound) ]
                #
                boxplot_width=1050  # Set width to 700 pixels
                boxplot_height=500  # Set height to 600 pixels
                cols = ['country_names','average_cost_for_two']
                y_axis_name = 'Preço do Prato para dois'
                df_aux = df_aux[ cols ].dropna()
                col1, col2 = st.columns( [3, 1])
                with col1:
                    fig = boxplotChart( df_aux , cols , y_axis_name , boxplot_width, boxplot_height )
                    st.plotly_chart( fig , use_container_width=True )
                with col2:
                    if len( outliers ) > 0:
                        st.markdown( " Outliers não estão no gráfico ao lado: " )
                        st.dataframe( outliers.style.highlight_max(axis=0) , use_container_width=True  )
                    else:
                        markdown_content = f'<p style="text-align: justify; margin-left:20px;"> Não há outliers para a seleção atual </p>'
                        st.markdown(  markdown_content , unsafe_allow_html = True  )
            else:
                boxplot_width=1050  # Set width to 700 pixels
                boxplot_height=500  # Set height to 600 pixels
                cols = ['country_names','average_cost_for_two']
                y_axis_name = 'Preço do Prato para dois'
                df_aux = df_aux[ cols ].dropna()
                col1, col2 = st.columns( [3, 1])
                with col1:
                    fig = boxplotChart( df_aux , cols , y_axis_name , boxplot_width, boxplot_height )
                    st.plotly_chart( fig , use_container_width=True )
                with col2:
                    st.markdown( " " ) 
        else:
            markdown_content = f'<p style="text-align: center;">  <br> <br> <br>  Selecione ao menos <br> um país e uma categoria de preço <br> para mostrar a distribuição dos preços </p>'
            st.markdown(  markdown_content,  unsafe_allow_html=True  )
    #