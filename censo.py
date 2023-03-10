from dash import dcc,html,Dash, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


app = Dash(__name__)
server=app.server
df= pd.read_csv("TB_POBLACION_INEI.csv")




pordepar= df.groupby(["Departamento", "Sexo"]).Cantidad.sum().reset_index()

#pandas.reset_index in pandas is used to reset index of the dataframe object to default indexing (0 to number of rows minus 1) or to reset multi level index. By doing so, the original index gets converted to a column.

#fig = px.bar(pordepar, x="Departamento", y ="Cantidad")

""" 
fig.update_layout(
    #plot_bgcolor = 'white',
    font_color= '#7FDBFF'
)
"""

app.layout = html.Div(children= [

    html.H1("POBLACION PERU 2021", style = {"textAlign": "center"}),

    html.Div([
    html.P("Data disponible en :  ",  style = {"textAlign": "center", 'display': 'inline-block'}),
    html.A("    https://www.datosabiertos.gob.pe/dataset/poblaci%C3%B3n-peru", href='https://www.datosabiertos.gob.pe/dataset/poblaci%C3%B3n-peru', target="_blank" , 
           style = {"textAlign": "center", 'display': 'inline-block', "marginLeft": "5px"}),
        ], style = {"textAlign": "center"}),

    html.Div([
    
    html.Div([
    html.Label(["Selecciona el Genero"], style = {"textAlign": "center", "margin-bottom": "50px", 'font-weight': 'bold'}),
    dcc.Dropdown(
        df["Sexo"].unique(), #valores que toma
        value="M", #Default
        id="genero-input", #se integra al input
    )], style= {"width":"20%", "marginLeft": "100px" , "marginTop": "30px" }),

    html.Div([
    dbc.Card(
    dbc.CardBody([
            html.H3("Total de Personas", className="card-title"),
            html.P(id="total", className="card-text")

    ] , className="border-start border-success border-5")
    )], style= {"marginLeft": "900px","textAlign": "center",
                "borderStyle": "solid",  "padding": "10px"   }),

    ], style = {"display": "flex"}
    ),

    dcc.Graph(
        id="barplot",
    ),

    html.Div([
    dcc.Graph(
        id= "pie-graph" , style={'display': 'inline-block'}
    ),

    dcc.Graph(
        id= "pie-graphtwo" , style={'display': 'inline-block'}
    )
    ])

])

@app.callback(
    Output("barplot", "figure"), #figura
    Output("total", "children"), #td: celda de tabla
    Input("genero-input", "value"),
   
)
def update(genero): #aca entra como argumento value que se encarga de crear la figura y calcular el total, se asigna segun el orden de output y el return
    filter_df=pordepar[pordepar.Sexo == genero]

    fig = px.bar(filter_df, x= "Departamento", 
                 y="Cantidad")
    
    fig.update_layout(title='<b>Numero de personas por Departamento </b>', title_x=0.5,
                          title_font_color="grey", yaxis_title="Numero de personas (M:millones)")
    #pie=px.pie(filter_df, values="Edad_Anio", names="Edad_Anio")
    
    return fig, filter_df.Cantidad.sum()

#HOVER DATA
@app.callback(
    Output("pie-graph", "figure"),
    Output("pie-graphtwo", "figure"),
    Input("barplot", component_property="hoverData"),
    Input("genero-input", "value"),

)
def update_pie(hov_data, genero):
    if hov_data is None: #cuando no seleccionas nada
        df_pie = df[(df.Sexo == genero) & (df.Departamento == "LIMA")]
        #print(df_pie)
        pie=px.pie(df_pie, values="Cantidad", names="Edad_Anio" , 
                   custom_data=["Cantidad", "Edad_Anio"])

        pie.update_traces(
        hovertemplate= "Rango de años : %{label} <br>Numero de personas: %{value} "
        )

        pie.update_layout(title='<b>Grupo de edades por Departamento: LIMA</b>', title_x=0.5,
                          title_font_color="grey")
        

        #pie two 
        pietwo=px.pie(df_pie, values="Cantidad", names="Provincia" , 
                   custom_data=["Cantidad", "Provincia"])

        pietwo.update_traces(
        hovertemplate= "Rango de años : %{label} <br>Numero de personas: %{value} "
        )

        pietwo.update_layout(title='<b>Numero de personas por Provincia: LIMA </b>', title_x=0.5,
                          title_font_color="grey")


        return pie, pietwo

    else:
        #print(hov_data)
        hov_departamento = hov_data['points'][0]['x']
        df_pie_hover = df[(df.Departamento == hov_departamento) & (df.Sexo == genero)]

        pie=px.pie(df_pie_hover, values="Cantidad", names="Edad_Anio" , 
                   custom_data=["Cantidad", "Edad_Anio"])

        pie.update_traces(
        hovertemplate= "Rango de años : %{label} <br>Numero de personas: %{value} "
        )

        pie.update_layout(title=f'<b>Grupo de edades por Departamento: {hov_departamento}</b>', title_x=0.5,
                          title_font_color="grey")


        #pie two 
        pietwo=px.pie(df_pie_hover, values="Cantidad", names="Provincia"
                   )

        pietwo.update_traces(
        hovertemplate= "Rango de años : %{label} <br>Numero de personas: %{value} "
        )

        pietwo.update_layout(title=f'<b>Numero de personas por Provincia: {hov_departamento}</b>', title_x=0.5,
                          title_font_color="grey")



        return pie, pietwo

if __name__ == "__main__":
    app.run_server(debug=True)
