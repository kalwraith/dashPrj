from py_src.project.project_layout import ProjectLayout
from py_src.project.networkx.project_networkx import ProjectNetworkx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, Dash, dcc
import plotly.express as px
import pandas as pd

class MainDash():
    def __init__(self):
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
        self.app.config.suppress_callback_exceptions = True
        self.set_layout()
        self.define_callback()
        self.project_layout = ProjectLayout(self.app)
        self.project_networkx = ProjectNetworkx(self.app)

    def start_server(self):
        if __name__ == '__main__':
            self.app.run_server(debug=True, port=5000)

    def set_layout(self):
        self.app.layout = dbc.Container([
            dcc.Location(id='url'),
            dbc.Row([
                dbc.Col(self.get_sidebar_html(), width=2),
                dbc.Col(self.get_main_content_html(), width=10)
            ])
        ], fluid=True, class_name='g-0')

    def get_sidebar_html(self):
            return dbc.Card([
                dbc.CardBody([
                    html.H4("Sidebar", className="display-9"),
                    html.Hr(),
                    html.P(
                        "Number of xxxx"
                    ),
                    dbc.Nav(
                        [
                            dbc.NavLink([html.I(className='fa fa-address-card'),"Profile"], href="/", active="exact"),      #active=exact인 경우 현재 페이지와 일치할 경우에만(=클릭) 색상입힘
                            dbc.NavLink([html.I(className='fa fa-diagram-project'),"Project"], href="/project", active="exact")
                        ],
                        vertical=True,
                        pills=True

                    ),
                ]),
            ],color='light', style=self.get_sidebar_style())

    def get_main_content_html(self):
        return html.Div(
            id='page-content',
            children=[],
            style=self.get_content_style()
        )

    def get_sidebar_style(self):
        SIDEBAR_STYLE = {
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'bottom': 0,
            'width': '12rem',
            'padding': '0rem 1rem',
            'background-color': '#f8f9fa'
        }
        return SIDEBAR_STYLE

    def get_content_style(self):
        CONTENT_STYLE = {
            'margin-left': '0rem',
            'margin-right': '2rem',
            'padding': '0rem 1rem'
        }
        return CONTENT_STYLE

    def define_callback(self):
        self.app.callback(
            Output("page-content", 'children'),
            [Input("url", "pathname")]
        )(self.render_page_content)

    def render_page_content(self, pathname):
        if pathname == '/':
            return [
                html.H1('Main Contents',style={'text-align':'center'}),
                dcc.Graph(id='bargraph',
                          figure=px.bar(pd.DataFrame({'years':[2020,2021,2022],'count':[4,5,6]}),x='years',y='count')
                          )
            ]
        elif pathname == '/project':
            return [
                self.project_layout.get_layout()
            ]

        elif pathname == '/project/networkx':
            return [
                self.project_networkx.get_layout()
            ]


main_dash = MainDash()
main_dash.start_server()