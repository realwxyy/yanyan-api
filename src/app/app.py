from flask import Flask, request
from src.config.config import DevelopmentConfig, ProductionConfig
from src.controller import register_all_blueprint
from src.utils.database import db
from src.utils import util
import time

app = Flask(__name__)
# ERROR: Working outside of application context
# app_ctx = app.app_context()
# app_ctx.push()
# app.config.from_object(DevelopmentConfig)
app.config.from_object(ProductionConfig)
# register blueprint
register_all_blueprint(app)


# 可以使用 @app.before_request 切面编程的方式修饰方法
# 也可以使用 app.before_request(method) 的方式挂载方法
@app.before_request
def before_request():
    '''
    @ desc: logger info before request (AOP)
    @ param: request
    @ return: not needed
    @ author: wxyy
    '''
    data = util.pack_params(request)
    url = request.base_url
    method = request.method
    params = []
    for k, v in data.items():
        params.append(str(k) + ':' + str(v))
    params_str = ','.join(params)
    now_time = time.time()
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now_time))
    request.start_time = now_time
    util.logger_of_begin(dict(u=url, m=method, p=params_str, s=start_time))


@app.after_request
def after_request(response, *args, **kwargs):
    '''
    @ desc: logger info after request (AOP)
    @ param: request
    @ return: not needed
    @ author: wxyy
    '''
    response = util.cross_domain_configuration(response)
    start_time = request.start_time
    now_time = time.time()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now_time))
    diff_time = str(round(now_time - start_time, 3))
    util.logger_of_end(dict(e=end_time, d=diff_time))
    return response

# @app.route('/upload', methods=['post'])
# def upload():
#     return 1234

db.init_app(app)
