import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np

#panels import
import panels.electionMap

def toLength(code, expectedLength):
    return "0"*(expectedLength-len(code)) + str(code)

app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
dataset = pd.read_csv("data/votes_departements.csv")


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    
    dcc.Graph(figure=panels.electionMap.panel(dataset.copy()))

])

if __name__ == '__main__':
    app.run_server(debug=True)