from py_src.project.create_dash import CreateDash
from dash import html
import dash_bootstrap_components as dbc

class ProjectDash(CreateDash):
    def __init__(self):
        super().__init__('/project')
        self.set_layout()


    def set_layout(self):
        self.app.layout = html.Div(
            [self.get_networkx_card()
             ]
        )




    def get_networkx_card(self):
        card = dbc.Card(
            [
                dbc.CardImg(src="/static/images/networkx.jpeg", top=True),
                dbc.CardBody(
                    [
                        html.H4("뉴스 키워드 시각화", className="card-title"),
                        html.P(
                            "뉴스 크롤링 & 시각화",
                            className="card-text",
                        ),
                        dbc.Button("보러가기", color="primary"),
                    ]
                ),
            ],
            style={"width": "18rem"},
        )
        return card