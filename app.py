from flask import Flask
from main_dash import MainDash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

app = Flask(__name__)
app.secret_key = 'the random string'

main_dash = MainDash()


application = DispatcherMiddleware(
    app,
    {"/": main_dash.app.server
     }
)

if __name__ == '__main__':
    # 미리 만들어 놓은 모델을 불러오는 곳
    # model = load_model('C:\xxxx\xxxxx.pb)
    #
    run_simple("192.168.0.3", 5000, application)