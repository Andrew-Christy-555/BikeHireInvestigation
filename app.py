from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import pandas as pd
df = pd.read_csv("assets/finalDataset.csv")

min_obesity=df["Obesity Percentage (18+)"].min()
max_obesity=df["Obesity Percentage (18+)"].max()
min_overweight=df["Overweight Percentage (18+)"].min()
max_overweight=df["Overweight Percentage (18+)"].max()
min_dockingLAD=df["Num Docking Stations Local Authority Districts"].min()
max_dockingLAD=df["Num Docking Stations Local Authority Districts"].max()
min_dockingMSOA=df["Num Docking Stations MSOAs"].min()
max_dockingMSOA=df["Num Docking Stations MSOAs"].max()
max_meanIMD=df["IMD mean"].max()
min_meanIMD=df["IMD mean"].min()

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1(
            children='Exploring Potential Areas for New Bike Hire Docking Stations',
            style={
                'textAlign': 'center','color':'red',
            }
        ),
        html.Div([
            html.H4(
                children='This app allows the exploration of population deprivation, obesity and overweight statistics, for Local Authority Districts. It also shows the number of bike docking stations within the Local Authority Districts (LAD) and Middle Super Output Areas (MSOA). Please select the ranges for each of these parameters and the table will update with the MSOAs and LADs that fit within those ranges. The table can also be sorted by any of the columns',
                style={
                        'textAlign': 'left','margin-left':'30px',
                }
            ),
        ]),
            html.Div([
                html.Label("% population overweight"),
                dcc.RangeSlider(
                    min=0,
                    max=max_overweight,
                    step=0.1,
                    value=[min_overweight,max_overweight],
                    id="ovr_slider",
                    updatemode='drag',
                    marks=None,
                    tooltip={"placement": "top", "always_visible": True},
                ),
                html.Label("% population obese"),
                dcc.RangeSlider(
                    min=0.0,
                    max=max_obesity,
                    step=0.1,
                    value=[min_obesity,max_obesity],
                    id="obs_slider",
                    updatemode='drag',
                    marks=None,
                    tooltip={"placement": "top", "always_visible": True},
                ),
                html.Label("Docking Stations Local Authority Districts"),
                dcc.RangeSlider(
                    min=0,
                    max=max_dockingLAD,
                    step=1,
                    value=[min_dockingLAD,max_dockingLAD],
                    id="numDockLADs_slider",
                    updatemode='drag',
                    marks=None,
                    tooltip={"placement": "top", "always_visible": True},
                ),
                ],style={'width':'80%','margin-left':'30px'}),
            html.Div([
                html.Label("Docking Stations MSOAs"),
                dcc.RangeSlider(
                    min=0,
                    max=max_dockingMSOA,
                    step=1,
                    value=[min_dockingMSOA,max_dockingMSOA],
                    id="numDockMSOAs_slider",
                    updatemode='drag',
                    marks=None,
                    tooltip={"placement": "top", "always_visible": True},
                ),
                html.Label("Mean Deprivation"),
                dcc.RangeSlider(
                    min=0.0,
                    max=max_meanIMD,
                    step=0.1,
                    value=[min_meanIMD,max_meanIMD],
                    id="IMD_mean_slider",
                    marks=None,
                    updatemode='drag',
                    tooltip={"placement": "top", "always_visible": True},
                ),
                html.Br(),
                ],style={'width':'80%','margin-left':'30px'})
        ]),
        html.Div([dash_table.DataTable(
                id='datatable-interactivity',
                editable=True,
                style_data={'height': 'auto'},
                style_table={'overflowX': 'scroll',       
                	'maxHeight': '900px',
			'overflowY': 'scroll'},
                style_cell={
                	'minWidth': '0px', 'maxWidth': '180px',
                	'whiteSpace': 'normal',
                },
                sort_action="native",
                sort_mode="multi",
                
                columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
                ],
                #data=df.to_dict('records')
            	),
                html.Div(id='datatable-interactivity-container')
        ])    
        ])

@app.callback(
        Output('datatable-interactivity','data'),
        [Input("ovr_slider", "value"),
        Input("obs_slider", "value"),
        Input("numDockLADs_slider","value"),
        Input("numDockMSOAs_slider", "value"),
        Input("IMD_mean_slider", "value")]
        )
def update_datatable(ovr,obs,numDocksLADs,numDocksMSOAs,dep):
   if ovr[0] is None:
        columns= [{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
        return data
   else:
        df_new = df.loc[(df['Obesity Percentage (18+)'] >= obs[0]) & (df['Overweight Percentage (18+)'] >= ovr[0])&(df['Num Docking Stations MSOAs']>=numDocksMSOAs[0]) & (df['Num Docking Stations Local Authority Districts'] >= numDocksLADs[0])  & (df['IMD mean']>=dep[0]) &(df['Obesity Percentage (18+)'] <= obs[1]) & (df['Overweight Percentage (18+)'] <= ovr[1])&(df['Num Docking Stations MSOAs']<=numDocksMSOAs[1]) & (df['Num Docking Stations Local Authority Districts'] <= numDocksLADs[1])  & (df['IMD mean']<=dep[1])]
        columns= [{"name": i, "id": i} for i in df_new.columns],
        data=df_new.to_dict('records')
        return data 

if __name__ == "__main__":
    app.run(debug=False)
