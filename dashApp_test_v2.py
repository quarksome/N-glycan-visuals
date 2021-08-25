# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 12:42:36 2020

@author: Nikko Bacalzo
Creates HTML Plotly app for visualizing EICs of N-glycans
Extracts graph objects from <filename>_allEIC.pickle, which is the output from Ngly_script

"""

# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import re
import pickle5 as pickle


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


##get all compounds
oligoLibraryFilename = 'N-Glycans_Hua.csv'
##READ OLIGO LIBRARY
oligoLib = pd.read_csv(oligoLibraryFilename, skiprows=range(29))  
oligoLib.rename(columns={'# Formula': 'Formula',
                         ' RT':'RT',
                         ' Mass': 'Mass',
                         ' Cpd': 'Cmpd_Label',
                         ' Comments': 'Type'}, inplace=True)
oligoLib = oligoLib[['Formula', 'Mass', 'Cmpd_Label', 'Type']]

cmpd_label_list = oligoLib['Cmpd_Label'].tolist()

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

cmpd_label_list.sort(key=natural_keys)

with open('HS_allEIC.pickle', 'rb') as handle:
    allEICDict = pickle.load(handle)



app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children='N-Glycan Analysis Script',
            style={
                'textAlign': 'center',
                'color': colors['text']
        }
    ),

    html.Div(children='Visualization of N-glycan chromatograms',
             style={
                'textAlign': 'center',
                'color': colors['text']
    }),
    
    dcc.Dropdown(
        id='cmpd-label',
        options=[{'label': x, 'value': x} for x in cmpd_label_list],
        value='5_2_0_0'   
    ),
    
    html.Div(id="output-text",
             style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
    html.Div(id='output-graphs', children=[])
])


@app.callback(
    [Output('output-text', 'children'),
     Output('output-graphs', 'children')],
    [Input('cmpd-label', 'value')])
def update_output(cmpd_label):
    all_plots = allEICDict[cmpd_label]
    graphList = []
    
    for idx, fig in enumerate(all_plots):
        graphList.append(dcc.Graph(
            id='graph-'+str(idx+1),
            figure=fig
            )
        )
    
    outText = "You are viewing EICs for {}".format(cmpd_label)
    return outText, graphList
    


if __name__ == '__main__':
    app.run_server(debug=True)

    
    
    