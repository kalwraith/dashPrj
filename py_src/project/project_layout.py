import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

class ProjectLayout():
    def __init__(self, app):
        self.app = app
        self.layout = self.get_project_main()

    def get_project_main(self):
        return dbc.Row([
            html.H3('Project History', style={'text-align': 'center'}),
            html.Br(),
            html.Br(),
            dbc.Col(dbc.Card([
                dbc.CardImg(src="static/images/networkx.jpeg", top=True),
                dbc.CardBody(
                    html.P("뉴스 네트워크 시각화", className="card-text")
                ),
                dbc.Button("보러가기", id='render_news_networkx', color="primary", href='/project/networkx')
                ],style={"width": "15rem", 'height':'15rem'}
            )),
            dbc.Col(dbc.Card([
                dbc.CardImg(src="static/images/lda_modeling.jpeg", top=True),
                dbc.CardBody(
                    html.P("LDA 토픽 모델링", className="card-text")
                ),
                dbc.Button("보러가기", id='render_news_lda', color="primary", href='/project/lda')
                ],style={"width": "15rem", 'height':'15rem'}
            ))
        ])

    def get_layout(self):
        return self.layout