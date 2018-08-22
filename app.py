# -*- coding: utf-8 -*-
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash, os
from dash.dependencies import Input, Output
from pymongo import MongoClient

MAPBOX_ACCESS_TOKEN = os.environ['MAPBOX_ACCESS_TOKEN']
MONGO_URI = os.environ['MONGO_URI']
#connect to MongoDB
mongo = MongoClient(MONGO_URI)
db = mongo.test

app = dash.Dash()

app.layout = html.Div([
	html.Div(
		dcc.Dropdown(
			id='team-select',
			options=[{'label': name, 'value': name} for name in db.rosters.distinct('teamname')],
			placeholder='Select a Team'
		),
	),
	html.Div(
		dcc.Graph(id='team-map'),
	)],
)

@app.callback(Output('team-map','figure'), [Input('team-select', 'value')])
def update_graph(dropdown_value):
    lon = []
    lat = []
    text = []
    if dropdown_value is not None:
        #query roster array matching teamname
        arr = db.rosters.find_one({'teamname':dropdown_value},{'_id':0})['roster']
        #convert roster to DataFrame
        df = pd.DataFrame(arr)
        #remove all players without location
        df = df[df['loc'] != '--']
        # convert loc to df
        loc = pd.DataFrame.from_records(df['loc'])
        lon = loc['lng']
        lat = loc['lat']
        text = +df['name']+'<br>'+df['class']+' '+df['pos']+' #'+df['no']+'<br>'+df['ht']+' '+df['wt']+'lbs<br>'+df['hometown']

    data = [ go.Scattermapbox(
        lon= lon,
        lat= lat,
        hovertext= text,
        hoverinfo= 'text',
        hoverlabel=dict(
            bgcolor = 'grey',
            bordercolor = 'black'
            ),
        mode = 'markers',
        marker=dict(
            size=4,
            color='red'
        ))
    ]

    layout = go.Layout(
        width=800,
        height=600,
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            bearing=0,
            center=dict(
                lat=38,
                lon=-107
            ),
        pitch=0,
        zoom=2,
        style='mapbox://styles/khallor1/cjkxj7ky146w22rp0umb6qmed'
        )
    )      
        
    return dict(data=data, layout=layout)

if __name__ == '__main__':
	app.run_server(debug=True)
