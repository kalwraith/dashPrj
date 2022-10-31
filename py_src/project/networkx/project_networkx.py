from py_src.project.networkx.run_apriori import RunApriori
from py_src.project.networkx.graph_networkx import GraphNetworkx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import ctx, dcc, html

class ProjectNetworkx():
    def __init__(self, app):
        self.app = app
        self.layout = self.get_project_network_layout()
        self.app_callback()
        self.selected_news_dt = ''

    def get_project_network_layout(self):
        return dbc.Tabs([
            dbc.Tab(children=[], label='이번달', id='cur-month'),
            dbc.Tab(children=self.sidebar_and_main(), label='월별', id='monthly-button'),
            dbc.Tab(label='분기별', tab_id='quarter-button'),
            dbc.Tab(label='연도별', tab_id='year-button')
            ], id='networkx_tabs',
            active_tab='monthly-button'
        )


    def sidebar_and_main(self):
        return dbc.Container([
            dbc.Row([
                dbc.Col(children=[], id='networkx_sidebar', width=2),
                #
                dcc.Loading(
                    id='networkx_main_loading',
                    children=self.get_main_toolbar()
                )
            ], class_name='g-2')
        ])



    def get_layout(self):
        return self.layout

    def app_callback(self):
        self.app.callback(
            Output('networkx_sidebar', 'children'),
            Input('monthly-button','n_clicks')
        )(self.get_sidebar_layout)

        # 기간 선택
        self.app.callback(
            Output('sel-news-dt','children'),
            [Input('navlink_201901', 'n_clicks'),
             Input('navlink_201902', 'n_clicks'),
             Input('navlink_201903', 'n_clicks')]
        )(self.set_news_dt)

        # layout 조정 callback
        self.app.callback(
            Output('networkx_main_loading', 'children'),
            Input('run-networkx', 'n_clicks'),
            [State('select-min-support','value'),
             State('sel-layout','value')]
        )(self.get_main_layout)
        
        
    def get_sidebar_layout(self, n_clicks):
        return dbc.Accordion([
                        dbc.AccordionItem([
                            dbc.Nav([
                                dbc.NavLink('1월', id='navlink_201901'),
                                dbc.NavLink('2월', id='navlink_201902'),
                                dbc.NavLink('3월', id='navlink_201903'),
                                dbc.NavLink('4월', id='navlink_201904'),
                                dbc.NavLink('5월', id='navlink_201905'),
                                dbc.NavLink('6월', id='navlink_201906'),
                                dbc.NavLink('7월', id='navlink_201907'),
                                dbc.NavLink('8월', id='navlink_201908'),
                                dbc.NavLink('9월', id='navlink_201909'),
                                dbc.NavLink('10월', id='navlink_201910'),
                                dbc.NavLink('11월', id='navlink_201911'),
                                dbc.NavLink('12월', id='navlink_201912')
                            ], vertical='sm')
                        ], title='2019'),
                        dbc.AccordionItem('2020년', title='2020'),
                        dbc.AccordionItem('2021년', title='2021'),
                        dbc.AccordionItem('2022년', title='2022')
                    ], always_open=False, start_collapsed=True)


    def get_main_toolbar(self):
        return dbc.Container([
                dbc.Row([
                    dcc.Markdown([], id='sel-news-dt'),
                ], class_name='g-0'),
                dbc.Row([
                    dbc.Col(html.P('Select Layout'), width=4),
                    dbc.Col(dcc.Dropdown(['circular','fruchterman_reingold','kamada_kawai','random','shell','spectral','spiral']
                                         , id='sel-layout'

                                         )
                            ,width=5),
                ], justify="start"),
                dbc.Row([
                    dbc.Col(dbc.Col(html.P('Select min support')), width=4),
                    dbc.Col(dcc.Slider(min=0.01,
                               max=0.05,
                               step=0.01,
                               value=0.02,
                               id='select-min-support'
                        ),width=5),
                    dbc.Col(dbc.Button("Show Graph", color="primary", id='run-networkx', size='sm'),width=3)
                ])
            ])

    def set_news_dt(self,  mon1, mon2, mon3):
        button = ctx.triggered_id if not None else None
        if button is not None:
            self.selected_news_dt = button.split('_')[1]
            return f'선택: {self.selected_news_dt}'
        else:
            return ''



    def get_main_layout(self,btn, min_support, sel_layout):
        if self.selected_news_dt != '201903':
            return dbc.Container([
                html.Br(),
                self.get_main_toolbar()
                ])
        else:
            run_apriori = RunApriori(self.selected_news_dt)
            apriori_rslt_df = run_apriori.get_apriori_rslt(min_support=min_support)
            graph_network = GraphNetworkx(apriori_rslt_df=apriori_rslt_df, layout=sel_layout)
            return dbc.Col([
                html.Br(),
                self.get_main_toolbar(),
                # dbc.Row([
                #     dcc.Graph(
                #             id='slider-graph',
                #             figure=graph_network.get_networkx_fig()
                #         )
                # ])
                dbc.Row([
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[
                            dcc.Graph(
                                id='slider-graph',
                                figure=graph_network.get_networkx_fig()
                            )
                        ]
                    )
                ])
            ])