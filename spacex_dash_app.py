# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites',
                                                     'value': 'ALL'},
                                                 {'label': launch_sites[0],
                                                     'value': launch_sites[0]},
                                                 {'label': launch_sites[1],
                                                     'value': launch_sites[1]},
                                                 {'label': launch_sites[2],
                                                     'value': launch_sites[2]},
                                                 {'label': launch_sites[3],
                                                     'value': launch_sites[3]},
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       2500: '2500',
                                                       5000: '5000',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df[spacex_df['class'] ==
                         1]['Launch Site'].value_counts().reset_index()
        data.columns = ['Launch Site', 'class']
        fig = px.pie(data, values='class',
                     names=data['Launch Site'],
                     title='Success Launches By Site')
        return fig
    else:
        data = spacex_df[spacex_df['Launch Site'] ==
                         entered_site]['class'].value_counts().to_frame().reset_index()
        fig = px.pie(data, values='count',
                     names=data['class'],
                     title=f'Success Launches For Site {entered_site}')
        return fig

        # TASK 4:
        # Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")]
              )
def get_scatter_plot(entered_site, entered_payload):
    if entered_site == 'ALL':
        data = spacex_df[(spacex_df['Payload Mass (kg)'] > entered_payload[0]) & (
            spacex_df['Payload Mass (kg)'] < entered_payload[1])]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Correlation between Payload and Success for all sites')
        return fig
    else:
        data = spacex_df[(spacex_df['Payload Mass (kg)'] > entered_payload[0]) & (
            spacex_df['Payload Mass (kg)'] < entered_payload[1])]
        data = data[data['Launch Site'] == entered_site]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Correlation between Payload and Success for Site {entered_site}')
        return fig


# Questions
# 1. Which site has the largest successful launches?
# R. KSC.LC-39A
# 2. Which site has the highest launch success rate?
# R. CCAFS SLC-40
# 3.Which payload range(s) has the highest launch success rate?
# R. 0-6000
# 4.Which payload range(s)has the lowest launch success rate?
# R. 6000-9000
# 5.Which F9 Booster version has the highest launch success rate?
# R. FT

        # Run the app
if __name__ == '__main__':
    app.run_server()
