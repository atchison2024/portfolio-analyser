import dash
from dash import dcc, html, Input, Output, State
import dash_table
import pandas as pd
import numpy as np

from utils import fetch_portfolio, calculate_portfolio_metrics

# Initial load
portfolio_df = fetch_portfolio()

app = dash.Dash(__name__)
app.title = "Portfolio Analyser"

# App layout
app.layout = html.Div([
    html.H1("Portfolio Analyser", style={"textAlign": "center"}),

    html.H2("Current Portfolio"),
    dash_table.DataTable(
        id='portfolio-table',
        columns=[{"name": i, "id": i} for i in ['asset', 'return', 'volatility', 'allocation']],
        data=portfolio_df.to_dict('records'),
        editable=False,
        style_table={'width': '60%'},
    ),

    html.H3("Add New Fund"),
    html.Div([
        dcc.Input(id='asset-name', type='text', placeholder='Fund name', debounce=True),
        dcc.Input(id='asset-return', type='number', placeholder='Expected return', debounce=True),
        dcc.Input(id='asset-vol', type='number', placeholder='Volatility', debounce=True),
        dcc.Input(id='asset-alloc', type='number', placeholder='Allocation $', debounce=True),
        html.Button("ADD", id="add-btn", n_clicks=0),
    ], style={"marginBottom": "20px"}),

    html.Button("ANALYSE", id="analyze-btn", n_clicks=0),

    html.Div(id="analysis-output", style={"marginTop": "30px", "fontSize": "18px"}),
])

# Callbacks
@app.callback(
    Output('portfolio-table', 'data'),
    Input('add-btn', 'n_clicks'),
    State('portfolio-table', 'data'),
    State('asset-name', 'value'),
    State('asset-return', 'value'),
    State('asset-vol', 'value'),
    State('asset-alloc', 'value'),
    prevent_initial_call=True,
)
def add_new_asset(n_clicks, table_data, name, ret, vol, alloc):
    if name and ret is not None and vol is not None and alloc is not None:
        table_data.append({
            "asset": name,
            "return": float(ret),
            "volatility": float(vol),
            "allocation": float(alloc)
        })
    return table_data

@app.callback(
    Output('analysis-output', 'children'),
    Input('analyze-btn', 'n_clicks'),
    State('portfolio-table', 'data'),
    prevent_initial_call=True,
)
def analyse_portfolio(n_clicks, data):
    df = pd.DataFrame(data)
    port_return, port_vol = calculate_portfolio_metrics(df)
    return f"📊 Portfolio Expected Return: {port_return:.2%} | 📉 Volatility: {port_vol:.2%}"

if __name__ == '__main__':
    app.run_server(debug=True)
