# Paquetes usados.
import pandas as pd
import numpy as np
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# Datasets
data_escala = pd.read_csv("data/data_escala.csv", index_col=0)
data_long = pd.read_csv("data/data_long.csv", index_col=0)
data_ext = pd.read_csv("data/data_ext.csv")

data_long["InstrumentosPromCant"] = data_long["Instrumentos"]/data_long["Cantidad"]
data_long["InstrumentosPromPeso"] = data_long["Instrumentos"]/data_long["Peso"]

#data_ext = data_ext.iloc[0:4550,:35]
data_ext = data_ext[['Class of Orbit', 'Perigee (km)', 'Apogee (km)','Launch Mass (kg.)', 'Dry Mass (kg.)']]

# Gráficos

# Creamos el mapa de colores vinculados a cada uno de los continentes.
color_map = {"Asia Central":" #8e44ad ",
             "America del Sur": " #2980b9 ",
             "Asia":" #cb4335 ",
             "Africa":" #27ae60 ",
             "Europa":"  #e67e22  ",
             "Resto America":" #17a589 "}

color_map_violin = {'LEO':'#05766E',
                    'GEO':'#C06B08'}


def plotTreemap1(variable):
    treemap = px.treemap(data_frame = data_long,
                          path = ['Continente', 'Pais', 'TipoSatelite'],
                          color = "Continente",
                          values = variable,
                          custom_data = ['Pais','Continente','TipoSatelite','Cantidad','Peso','Instrumentos'],
                          color_discrete_map = color_map)
    
    treemap.update_traces(hovertemplate = '<b>%{customdata[0]}</b> <br><br> Continente: %{customdata[1]} <br>'+f'{variable}'+': %{value:.}',
                          textinfo = 'label+value',
                          textfont = {'color':'white'})
    
    treemap.update_layout(
                        #   title = {'font':{'size':24},
                        #          'text':'Treemap Satélites - Cantidad',
                        #          'x':0.1,
                        #          'y':0.93},
                          hoverlabel = {'font':{'color':'white'}},
                          margin={'t':20, 'b':10, 'l':0, 'r':0},
                          template = 'plotly_white')
    
    return treemap

def plotScatter1(variable):
    
    df = data_long.copy()
    df = df[df["TipoSatelite"] == variable]
    
    scatter = px.scatter(data_frame = df,
                         x = "Peso",
                         y = "Instrumentos",
                         color = "Continente",
                         size = "Cantidad", 
                         custom_data = ["Pais", "Cantidad"],
                         color_discrete_map = color_map)
    
    scatter.update_traces(hovertemplate = "<b> %{customdata[0]} </b> <br> <br> Peso: %{x:.} <br> Instrumentos: %{y} <br> Cantidad: %{customdata[1]} <extra></extra>")
    
    scatter.update_layout(legend= {'itemsizing': 'constant',
                                   'orientation':'h',
                                   'y':1.1,
                                   'x':0.5,
                                   'xanchor':'center',
                                   'title':{'text':'<b>Continente</b>',
                                            'font':{'size':13}}},
                        #   title= {'text':f'<b>{variable}</b>',
                        #           'font':{'size':20},        
                        #            'xanchor':'left',
                        #            'y':0.92},
                          xaxis={'title':{'text':"Peso Total [kg]"}},
                          yaxis={'title':{'text':"Cantidad de Instrumentos"}},
                          margin={'l':0, 'r':0},
                          template='plotly_white')
    
    # scatter.add_annotation(text = f'<b>{variable}</b>',
    #                        font = {'size':20},
    #                        xref = 'x domain',
    #                        yref = 'y domain',
    #                        x = 0.95,
    #                        y = -0.16,
    #                        showarrow = False)
    
    return scatter

def selectP(variable):
    
    if variable == "LEO":
        text = '''
        Los satélites **LEO** son los de órbita terrestre baja llegando a una altitud máxima de 2.000 kilómetros. Aquí se ubican una gran cantidad de satélites meteorológicos y de comunicaciones. Tienen una alta velocidad respecto de la superficie terrestre y la resistencia de la débil atmósfera implica que deben ser reajustados en su órbita cada cierto tiempo.

        Para satélites **LEO** la relación entre peso y cantidad de instrumentos no es lineal, principalmente por el auge de microsatélites en baja órbita y menores costos de envío que permiten que nuevos países se inicien en el desarrollo de satélites de bajo peso pero con gran potencial en cuanto a capacidad (número de instrumentos).
        '''
    else: 
        text = '''
        Los satélites **GEO** son los de órbita terrestre alta u órbita geocéntrica que se ubica alrededor de los 35.800 kilómetros de altitud y permite tener un período orbital prácticamente coincidente con la duración de un día en la Tierra. Esto genera que estos satélites parezcan inmóviles en el espacio respecto de la superficie terrestre.
        
        Para satélites **GEO** la relación entre peso y cantidad de instrumentos resulta en gran medida lineal, tratándose de satélites más grandes, más equipados y de mayor potencia debido a su lejanía y funciones.
        '''
    return text

def plotViolin(check_vals):
    
    if 'Box' in check_vals:
        box_plot = True
    else:
        box_plot = False
        
    if 'Points' in check_vals:
        points_plot = 'all'
    else:
        points_plot = False
    
    
    df = data_ext.copy()
    df = df[df['Class of Orbit'].isin(['LEO','GEO'])]
    
    violin = px.violin(data_frame=df,
                       x = 'Class of Orbit',
                       y = 'Launch Mass (kg.)',
                       color = 'Class of Orbit',
                       box = box_plot,
                       points=points_plot, 
                       violinmode='overlay',       
                       color_discrete_map=color_map_violin)
    
    violin.update_traces(marker={'opacity':0.35, 
                                 'size':4},
                         hovertemplate="<b>%{x}</b> <br> Masa de Lanzamiento: %{y} kg<extra></extra>",
                         hoveron="points+violins")
                         #pointpos = -2,
                         #jitter = 0.4)
    
    violin.update_layout(legend= {'itemsizing': 'constant',
                                   'orientation':'v',
                                   'y':0.9,
                                   'x':0.8,
                                   'title':{'text':'<b>Órbita</b>',
                                            'font':{'size':13}}},
                         xaxis={'title':{'text':""},
                                'showticklabels':False},
                         yaxis={'title':{'text':"Masa de Lanzamiento [kg]"}},
                         margin={'t':0, 'b':20, 'l':0, 'r':0},
                         template='plotly_white')
    
    return violin

def plotScatter2(variable):
    
    df = data_long.copy()
    df = df[df["TipoSatelite"] == variable]
    
    scatter = px.scatter(data_frame = df,
                       x = "Peso Promedio",
                       y = "InstrumentosPromCant",
                       color = "Continente",
                       size = "Cantidad",
                       custom_data=["Pais", "Peso Promedio", "InstrumentosPromCant", "Cantidad"],
                       color_discrete_map=color_map)

    scatter.update_traces(hovertemplate = '<b>%{customdata[0]}</b> <br><br> Peso Promedio: %{customdata[1]:.2f} <br> Instrumentos Promedio: %{customdata[2]:.2f} <br> Cantidad: %{customdata[3]}<extra></extra>',
                          opacity=1)

    scatter.update_layout(legend= {'itemsizing': 'constant',
                                   'orientation':'h',
                                   'y':1.1,
                                   'x':0.5,
                                   'xanchor':'center',
                                   'title':{'text':'<b>Continente</b>',
                                            'font':{'size':13}}},
                          xaxis={'title':{'text':"Peso Promedio [kg]"}},
                          yaxis={'title':{'text':"Instrumentos Promedio"}},
                          margin={'t':60, 'l':0, 'r':0},
                          template="plotly_white")
    
    # scatter.add_annotation(text = f'<b>{variable}</b>',
    #                        font = {'size':20},
    #                        xref = 'paper',
    #                        yref = 'paper',
    #                        x = 0.02,
    #                        y = 0.96,
    #                        showarrow = False)

    return scatter

def plotScatter3(variable1, variable2, variable3, log):
    
    if log == 'Linear':
        log = False
    else:
        log = True
    
    df = data_escala.copy().dropna()
    
    axis_label_dict = {'Total satélites':'Cantidad de Satélites',
                       'Total Instrumentos':'Cantidad de Instrumentos',
                       'PesoTotal':'Peso',
                       'Cantidad de Escalones': 'Cantidad de Escalones',
                       'Escalón más alto':'Escalón Máximo'}
    
    scatter = px.scatter(data_frame = df,
                         x = variable1,
                         y = variable2,
                         color = "Continente",
                         size = variable3,
                         custom_data=["Pais", "Escalón más alto", "Cantidad de Escalones", "Total satélites", "Total Instrumentos", "PesoTotal"],
                         log_x=log,
                         color_discrete_map=color_map)
    
    scatter.update_traces(hovertemplate = '<b>%{customdata[0]}</b> <br><br> Escalón Máximo: %{customdata[1]} <br> Cantidad Escalones: %{customdata[2]} <br> <br> Satélites: %{customdata[3]} <br> Instrumentos: %{customdata[4]} <br> Peso: %{customdata[5]}<extra></extra>',
                          opacity=1)

    scatter.update_layout(legend= {'itemsizing': 'constant',
                                   'orientation':'h',
                                   'y':1.1,
                                   'x':0.5,
                                   'xanchor':'center',
                                   'title':{'text':'<b>Continente</b>',
                                            'font':{'size':13}}},
                          xaxis={'title':{'text':f'{axis_label_dict[variable1]}'}},
                          yaxis={'title':{'text':f'{axis_label_dict[variable2]}'},
                                 'tickmode':'linear',
                                 'tick0':1,
                                 'dtick':1},
                          margin={'l':0, 'r':0},
                          template="plotly_white")

    return scatter



plotly_config = {'modeBarButtonsToRemove':['toImage', 'select', 'autoScale', 'lasso2D', 'zoomIn2d', 'zoomOut2d']}


    
# Dash App

app = Dash(__name__)
server = app.server

app.title = 'TIMMD - Viz'
app._favicon = ("satellite_icon.png")

# App Layout

app.layout = dbc.Container([
    
    dbc.Row([
        dbc.Col([
            # Título general.
            html.H1("Desarrollo de Tecnología Espacial - Argentina",
                    style = {'text-align':'center'}),
            # Párrafo de introducción.
            html.P("El desarrollo de tecnologías espaciales se encuentra en un gran auge este último tiempo. Los desarrollos actuales son producto de años de inversión e investigación en el sector. Argentina tiene una gran historia e importancia cuando analizamos países de características similiares incluyendo los de su región."),
            #html.Br(),
            html.P("Presentamos algunas visualizaciones que pueden ayudarnos a entender cómo es la dinámica del sector. También es importante entender que los distintos hitos en cuanto a la industria espacial que pueden llevar a cabo los países dependen de su inversión en el sector y estrategias específicas.")
            ],
            width = 12)
        ]),
    
    dbc.Row([
        dbc.Col(html.H2("Distribución de Satélites"))
        ]),
    
    dbc.Row([
       dbc.Col([dcc.Markdown("Con el siguiente gráfico podemos ver la distribución de los satélites en cada región analizada. Observando **cantidad**, **peso** y **número de instrumentos** destacamos la importancia de América Latina comparada con el resto de las regiones."),
                dcc.Markdown("Además de serparar por región y país el gráfico nos permite entender la magnitud de las características analizadas por cada tipo de satélites, **LEO** y **GEO**.")],
               width = 4),
       dbc.Col([dcc.Dropdown(id='dw_treemap1',
                             options=[{'label':'Cantidad',
                                       'value':'Cantidad'},
                                      {'label':'Peso',
                                       'value':'Peso'},
                                      {'label':'Instrumentos',
                                       'value':'Instrumentos'}],
                             value='Cantidad',
                             clearable=False,
                             style={'margin-bottom':'0px'},
                             className='dropdown_style'),
                dcc.Graph(id='treemap1',
                          figure=plotTreemap1('Cantidad'),
                          config={'modeBarButtonsToRemove':['toImage'],
                                  'displaylogo':False})],
               width=8) 
    ]),
    
    dbc.Row([
        dbc.Col(html.H2("LEO vs GEO"))
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='dw_scatter1',
                         options=[{'label':'LEO',
                                   'value':'LEO'},
                                  {'label':'GEO',
                                   'value':'GEO'}],
                         value='LEO',
                         clearable=False,
                         className='dropdown_style'),
            dcc.Graph(id='scatter1',
                      figure=plotScatter1('LEO'),
                      config = plotly_config)],
                width = 8),
        dbc.Col([dcc.Markdown(id='mkdw_1')],
                width = 4)
    ]),
    
    dbc.Row([
       dbc.Col([dcc.Markdown('''
                             Podemos ver la diferencia en la masa de lanzamiento de los satélites enviados a cada órbita. 
                             
                             Para el caso de satélites en **LEO** tenemos una mayor variedad de tamaños con una gran presencia de equipos pequeños, generando una distribución asimétrica. Igualmente tenemos satélites de gran tamaño como el caso del Hubble, de 11 toneladas.
                             
                             Los satélites en órbita **GEO** presentan una distribución de tamaños más acotada y uniforme, teniendo masas de lanzamiento que rondan generalmente entre los 2.000 y 6.000 kilogramos.
                             ''')],
               width = {'size':4, 'order':1}),
       dbc.Col([dcc.Checklist(options=[{'label':'Box',
                                        'value':'Box'},
                                       {'label':'Points',
                                        'value':'Points'}],
                              value=[],
                              id = 'check', 
                              className = 'check_container',
                              labelClassName = 'check_label',
                              inputClassName = 'check_input'),
                dcc.Graph(id='violin',
                          figure = plotViolin([]),
                          config = plotly_config)],
               width = {'size':8, 'order':2}) 
    ]),
    
    dbc.Row([
        dbc.Col(html.H2("Rendimiento"))
    ]),
    
    dbc.Row([
        dbc.Col(
            dcc.Markdown('''
                         Como medida de rendimiento podemos normalizar tanto la cantidad de instrumentos total y el peso total por la cantidad de satélites enviados. De esta manera, cuanto mayor sea el número de **Instrumentos Promedio** y menor sea el **Peso Promedio** mejor aprovechamiento del equipo enviado.
                         
                         Para satélites **LEO** vemos una menor cantidad de instrumentos por satélite, pero un mayor aprovechamiento de la carga enviada al ser de baja masa. 
                         
                         Por otro lados los satélites **GEO** son más complejos y grandes, por lo que poseen un mayor número de sensores pero una masa considerablemente mayor.
                         '''),
            width = 4
        ),
        dbc.Col([
            dcc.Dropdown(id='dw_scatter2',
                         options=[{'label':'LEO',
                                   'value':'LEO'},
                                  {'label':'GEO',
                                   'value':'GEO'}],
                         value='LEO',
                         clearable=False,
                             className='dropdown_style'),
            dcc.Graph(id='scatter2',
                      figure=plotScatter2('LEO'),
                      config=plotly_config)],
                width = 8)
    ]),
    
    dbc.Row([
        dbc.Col([dcc.Markdown('''
                              Es importante destacar que se puede asociar el costo de envío con el peso de la carga enviado al espacio. Igualmente este análisis es limitado porque no considera el nivel de complejidad de los instrumentos enviados ni costos de investigación y desarrollo.
                              '''),
                 html.H2("Escala STL"),
                 dcc.Markdown('''
                              Finalmente podemos analizar la escala *Space Technology Ladder* (STL) para observar cómo fue el desarrollo de los países incluídos en este trabajo en dicho sistema de hitos en tecnología espacial. Esta escala comienza en el punto 1 con la creación de una agencia espacial y termina en el escalón 13, indicando que el país tiene capacidad de lanzamiento de un satélite GEO.
                              
                              No necesariamente un país debe pasar por todos los escalones, podemos analizar también por cuántos escalones ha pasado para llegar al estado actual. Es importante aclarar que esta escala no considera la complejidad de los satélites construidos ni las tecnologías utilizadas.
                              
                              Podemos destacar a Argentina e Israel teniendo el escalón máximo entre los países analizados, estando en el número 11 indicando capacidad de desarrollo y construcción local de un satélite GEO.
                              ''')
        ])
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='dw_scatter3_1',
                             options = [{'label':'Cantidad de Satélites',
                                         'value':'Total satélites'},
                                        {'label':'Cantidad de Instrumentos',
                                         'value':'Total Instrumentos'},
                                        {'label':'Peso',
                                         'value':'PesoTotal'}],
                             value='Total satélites',
                             clearable=False,
                             className='dropdown_style'),
                width = 3),
        dbc.Col(dcc.Dropdown(id='dw_scatter3_2',
                             options = [{'label':'Escalón Máximo',
                                         'value':'Escalón más alto'},
                                        {'label':'Cantidad de Escalones',
                                         'value':'Cantidad de Escalones'}],
                             value='Escalón más alto',
                             clearable=False,
                             className='dropdown_style'),
                width = 3),
        dbc.Col(dcc.Dropdown(id='dw_scatter3_3',
                             options = [{'label':'Cantidad de Satélites',
                                         'value':'Total satélites'},
                                        {'label':'Cantidad de Instrumentos',
                                         'value':'Total Instrumentos'},
                                        {'label':'Peso',
                                         'value':'PesoTotal'}],
                             value='PesoTotal',
                             clearable=False,
                             className='dropdown_style'),
                width = 3),
        dbc.Col(dcc.Dropdown(id='dw_scatter3_4',
                             options = [{'label':'Escala Lineal',
                                         'value':'Linear'},
                                        {'label':'Escala Log',
                                         'value':'Log'}],
                             value='Linear',
                             clearable=False,
                             className='dropdown_style'),                
                width = 3)
        # dbc.Col(html.Button('Log Scale',
        #                     id='bt_scatter3',
        #                     n_clicks = 0),
        # dbc.Col(dcc.RadioItems(id='ri_scatter3',
        #                        options = [{'label':'X Linear',
        #                                    'value':'Linear'},
        #                                   {'label':'X Log',
        #                                    'value':'Log'}],
        #                        value='Linear',
        #                        className='radio-item'),

    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='scatter3',
                          figure=plotScatter3('Total satélites', 'Escalón más alto', 'PesoTotal', 'Linear'),
                          config=plotly_config))
    ]),
    
    dbc.Row([
        dbc.Col()
    ])
    
])

# Callbacks
# Callback para el Dropdown del Treemap.
@app.callback(
    Output(component_id='treemap1',
           component_property='figure'),
    Input(component_id='dw_treemap1',
          component_property='value'),
    prevent_initial_callback=True
)
# Usando la función que arma el treemap actualizamos la variable graficada.
def updateTreemap1(selection):
    treemap = plotTreemap1(selection)
    return treemap

@app.callback(
    Output(component_id='scatter1',
           component_property='figure'),
    Output(component_id='mkdw_1',
           component_property='children'),
    Input(component_id='dw_scatter1',
          component_property='value'),
    prevent_initial_callback=True
)
def updateScatter1(selection):
    scatter = plotScatter1(selection)
    text = selectP(selection)
    return scatter, text

@app.callback(
    Output(component_id='violin',
           component_property='figure'),
    Input(component_id='check',
          component_property='value'),
    prevent_initial_callback=True
)
def updateViolin(selection):
    violin = plotViolin(selection)
    return violin

@app.callback(
    Output(component_id='scatter2',
           component_property='figure'),
    Input(component_id='dw_scatter2',
          component_property='value'),
    prevent_initial_callback=True
)
def updateScatter2(selection):
    scatter = plotScatter2(selection)
    return scatter


@app.callback(
    Output(component_id='scatter3',
           component_property='figure'),
    Input(component_id='dw_scatter3_1',
           component_property='value'),
    Input(component_id='dw_scatter3_2',
           component_property='value'),
    Input(component_id='dw_scatter3_3',
           component_property='value'),
    Input(component_id='dw_scatter3_4',
           component_property='value'),
    prevent_initial_callback=True
)
def updateScatter3(selection1, selection2, selection3, log_selection):
    scatter = plotScatter3(selection1, selection2, selection3, log_selection)
    return scatter


# Run app
if __name__ == '__main__':
    app.run_server(debug=True)





