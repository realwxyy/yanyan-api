from flask import Blueprint, make_response, jsonify, request
from src.utils import util, resp

t = Blueprint('test', __name__, url_prefix='/test')


@t.route('/t1', methods=['get'])
def t1():
    """
    @api {post} /api/v1.0/users 注册
    @apiVersion 0.0.0
    @apiName register_user
    @apiGroup Users
    @apiParam {String}  mobile      (必须)    用户手机号
    @apiParam {String}  password    (必须)    用户密码
    @apiParam {String}  sms_code    (必须)    用户短信验证码
    """
    return 'welocome to /test/t1'


@t.route('/t2', methods=['post'])
def t2():
    return 'welcome to /test/t2'

# 模拟请求接口成功的参数


@t.route('/t3', methods=['get'])
def t3():
    # return {'code': 200, 'msg': '成功', 'data': []}
    return make_response(jsonify({'code': 200, 'msg': '成功', 'data': []}))

@t.route('/t4', methods=['post'])
def t4():
    data = util.pack_params(request)
    return resp.resp_succ(data, message='添加成功')
