# 导入依赖包
from flask import request, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import response as resp
import functools

# AOP can only be called after logging in
# 登录拦截


def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.headers["common-token"]
        except Exception:
            # 没接收的到token,给前端抛出错误
            # 这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            # return jsonify(code=4103, msg='缺少参数token')
            return resp.resp_unauthorized({}, '缺少参数token')
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            s.loads(token)
        except Exception:
            # return jsonify(code=4101, msg="登录已过期")
            return resp.resp_unauthorized({}, '登录已过期')
        return view_func(*args, **kwargs)

    return verify_token


def gen_token(params):
    # 用 用户信息加密生成token
    # 过期时间为 60s * 60m * 24h * 30d
    # .decode("ascii")必加 一下午就解决这个 bug 了 不然是 byte 类型 jsonify 方法无法转换byte类型
    # s = Serializer(current_app.config['SECRET_KEY'], 60 * 60 * 24 * 31)
    s = Serializer(current_app.config['SECRET_KEY'], 30)
    token = s.dumps(params).decode("ascii")
    return token


def decrypt_token(token):
    # 用 3rd_session 解密生成 openId 和 session_key
    s = Serializer(current_app.config['SECRET_KEY'])
    params = s.loads(token)
    return params


def decrypt_token_from_reqeust(req):
    token = req.headers["common-token"]
    return decrypt_token(token)