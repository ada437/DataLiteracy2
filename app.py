#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 09:40:00 2019

@author: anna_amato
"""

import json
import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from dash.dependencies import Input, Output, State
import flask
import dash_bootstrap_components as dbc
import plotly.express as px

cyto.load_extra_layouts()
external_stylesheets =['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__,external_stylesheets=external_stylesheets,
meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server


authors=pd.read_csv("nodes_authors.csv")
poster=pd.read_csv("poster.csv")
dimensions = ["x", "y", "color"]
dimensions2 = ["z", "w", "color2"]
col_options = [dict(label=x, value=x) for x in authors.columns]
col_options2 = [dict(label=z, value=z) for z in poster.columns]



###############app layout elements 
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("HomePage", href='/homepage'),
                dbc.DropdownMenuItem("Bar Graphs", href='/bargraphs'),
                dbc.DropdownMenuItem("Social Network", href='/socialnetwork')
            ],
        ),
    ],
    brand="DataLiteracy CoDesign",
    brand_href="#",
    sticky="top",
)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Gallery Walk"),
                        html.H3(
                            """\
                            Data Visualizations"""
                        ), 
      
                                html.Div(
                                        [html.P([d + ":", dcc.Dropdown(id=d, options=col_options)])
                                        for d in dimensions],
                                        className="dropdown",
                                        ),
                                html.Div(
                                        [html.P([e + ":", dcc.Dropdown(id=e, options=col_options2)])
                                        for e in dimensions2],
                                        className="dropdown",
                                        ),
                                ],
                                md=4,
                                ),
                dbc.Col(
                    [
                        
                                html.Div(id='clustergram-control-tabs', className='control-tabs', children=[
                                        dcc.Tabs(id='clustergram-tabs', value='what-is', children=[
                                                dcc.Tab(label='Participants',
                                                        children=html.Div([
                                                                dcc.Graph(id="graph", className="bar", style={"width": "75%", "display": "inline-block"}),
                                                                ]),
                                                        
                                                        ), 
                                                dcc.Tab(label='Posters',
                                                        children=html.Div([
                                                                dcc.Graph(id="graph2", className="bar", style={"width": "75%", "display": "inline-block"}),
                                                                ]
                                )
                                )
                    ])
            ])
                                ])
                                ]) 
                                ],
    className="mt-4",
                                )
    


################ Declare app layout
app.layout = html.Div(children= [navbar, body])  


        
##########styles callback 
@app.callback(Output("graph", "figure"), [Input(d, "value") for d in dimensions])
def make_figure(x, y, color):
    return px.bar(
        authors,
        x=x,
        y=y,
        color=color,
        height=400,
    )

@app.callback(Output("graph2", "figure"), [Input(e, "value") for e in dimensions2])
def make_figures(x, y, color):
    return px.bar(
        poster,
        x=x,
        y=y,
        color=color,
        height=400,
    )

#element callback -- help
#@app.callback(Output('cytoscape-images', 'elements'),
#              [Input('dropdown-update-nodes', 'value')],
#              [State('cytoscape-images', 'elements')])
    
#def update_elements(elements):
#    
#    filtered_weighted = weightedlinks2[weightedlinks2['c'] == elements]
#    return len(filtered_weighted)
    


#@app.server.route('/images/<image_path>.png')
#def serve_image(image_path):
#    image_name = '{}.png'.format(image_path)
#    return flask.send_from_directory("images", image_name)


if __name__ == '__main__':
    app.run_server(debug=True)