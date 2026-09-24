import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
from starlette.middleware.wsgi import WSGIMiddleware

from app.database import mongo_client, redis_client
from app.routes.charts import get_asset_chart

# requests_pathname_prefix routes all internal Dash requests under /dashboard/
dash_app = dash.Dash(
    __name__,
    requests_pathname_prefix="/dashboard/",
    routes_pathname_prefix="/dashboard/"
)

dash_app.layout = html.Div(
    style={
        "fontFamily": "Inter, system-ui, sans-serif",
        "backgroundColor": "#0f172a",
        "color": "#f8fafc",
        "minHeight": "100vh",
        "padding": "32px",
    },
    children=[
        html.Div(
            style={"maxWidth": "1200px", "margin": "0 auto"},
            children=[
                # Header
                html.Div(
                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "24px"},
                    children=[
                        html.Div([
                            html.H1("Market Analytics", style={"margin": "0", "fontSize": "26px", "fontWeight": "700"}),
                            html.P("FastAPI + Redis + Pandas + Plotly Dash", style={"margin": "4px 0 0 0", "color": "#94a3b8", "fontSize": "14px"}),
                        ]),
                        # Source Indicator Pill
                        html.Div(id="source-indicator", style={"padding": "8px 16px", "borderRadius": "24px", "fontWeight": "600", "fontSize": "13px"})
                    ]
                ),

                # Control Bar
                html.Div(
                    style={"backgroundColor": "#1e293b", "padding": "16px 20px", "borderRadius": "12px", "display": "flex", "alignItems": "center", "gap": "16px", "marginBottom": "24px"},
                    children=[
                        html.Label("Select Asset:", style={"fontWeight": "600", "fontSize": "14px"}),
                        dcc.Dropdown(
                            id="asset-dropdown",
                            options=[
                                {"label": "Bitcoin (BTC)", "value": "BTC"},
                                {"label": "Apple (AAPL)", "value": "AAPL"}
                            ],
                            value="BTC",
                            clearable=False,
                            style={"width": "220px", "color": "#0f172a"}
                        )
                    ]
                ),

                # Chart Display
                html.Div(
                    style={"backgroundColor": "#1e293b", "padding": "20px", "borderRadius": "12px"},
                    children=[
                        dcc.Loading(
                            type="dot",
                            color="#38bdf8",
                            children=[dcc.Graph(id="price-chart", config={"displayModeBar": False})]
                        )
                    ]
                )
            ]
        )
    ]
)

@dash_app.callback(
    [Output("price-chart", "figure"),
     Output("source-indicator", "children"),
     Output("source-indicator", "style")],
    [Input("asset-dropdown", "value")]
)
def update_chart(symbol):
    # Re-use our cached chart generator directly
    db = mongo_client["market_db"]
    result = get_asset_chart(symbol=symbol, db=db, cache=redis_client)
    
    chart_payload = result["chart"]
    source = result["source"]
    
    # Reconstruct Plotly figure and apply consistent dark styling
    fig = go.Figure(chart_payload)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1e293b",
        plot_bgcolor="#1e293b",
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    if source == "redis_cache":
        badge_text = "⚡ Cached via Redis"
        badge_style = {"backgroundColor": "#14532d", "color": "#4ade80", "border": "1px solid #22c55e"}
    else:
        badge_text = "🔄 Aggregated via MongoDB & Pandas"
        badge_style = {"backgroundColor": "#1e3a8a", "color": "#60a5fa", "border": "1px solid #3b82f6"}

    return fig, badge_text, badge_style

# Export the WSGI-wrapped instance for FastAPI
dash_mount = WSGIMiddleware(dash_app.server)