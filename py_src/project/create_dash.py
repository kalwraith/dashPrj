from dash import Dash, html
import dash_bootstrap_components as dbc
class CreateDash():
    def __init__(self, url):
        self.app = Dash(requests_pathname_prefix=f"{url}",
                        serve_locally=False,
                        external_stylesheets=dbc.themes.BOOTSTRAP)

    def set_layout(self):
        '''
        자식클래스에서 작성
        '''
        pass

