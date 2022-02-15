from flask import current_app
from marshmallow.fields import Date
from werkzeug.utils import secure_filename
from src.common import CONS
from .logger import logger
import datetime
import time
import json
import os


def cross_domain_configuration(resp):
    '''
    @ desc: Cross-domain configuration
    @ param: response
    @ return: none
    @ author: wxyy
    '''
    # 跨域配置
    resp.headers['Access-Control-Allow-Origin'] = '*' # admin
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,OPTIONS,POST,PUT,DELETE'
    resp.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, common-token'
    return resp


def logger_of_begin(info):
    '''
    @ desc: get information before request
    @ param: url & method & param_str & start_time (all required)
    @ return: not needed
    @ author: wxyy
    '''
    logger.info('请求开始 :O')
    logger.info('------------------------------')
    logger.info('请求地址:【 %s 】' % (info['u']))
    logger.info('请求方式:【 %s 】' % (info['m']))
    logger.info('请求参数:【 %s 】' % (info['p']))
    logger.info('请求开始时间:【 %s 】' % (info['s']))


def logger_of_end(info):
    '''
    @ desc: get information after request
    @ param: end_time & diff_time (all required)
    @ return: not needed
    @ author: wxyy
    '''
    logger.info('请求结束时间:【 %s 】' % (info['e']))
    logger.info('请求耗时:【 %s s】' % (info['d']))
    logger.info('------------------------------')
    logger.info('请求结束 :)')


def filter_param(params, key_arr):
    '''
    @ desc: filter parameter from customer
    @ param: params: params from customer
    @ param: key_arr: needed parameter
    @ return: dict of valid parameter
    @ author: wxyy
    '''
    return {o: params.get(o) for o in key_arr if params.get(o) != None}


def dict_not_empty(params, key_arr):
    '''
    @ desc: valid params not empty
    @ param1: params: valid dict
    @ param2: key_arr: valid list of key
    @ author: wxyy
    '''
    default_list = [o for o in key_arr if not (params.get(o) or params.get(o) == 0)]
    list_length = len(default_list)
    default_msg = ' , '.join(default_list)
    return_msg = '参数 [ ' + default_msg + ' ] 不可为空' if list_length > 0 else ''
    code = -1 if list_length > 0 else 0
    return dict(code=code, msg=return_msg)


def validate_dict_not_empty_with_key(params, key_arr):
    '''
    @ desc 验证参数是否为空
    @ param params 要验证的dict
    @ param key_arr 要验证的key的list
    '''
    msg = []
    code = 0
    for k in key_arr:
        if not all([params.get(k)]):
            code = -1
            msg.append('参数 [' + k + '] 不可为空')
    return {'code': code, 'msg': msg}


def convert_date(param=''):
    '''
    @ desc: give default if empty and convert date type
    @ param: date(type: datetime date time)
    @ return: fomatter value
    @ author: wxyy
    '''
    res = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    t = type(param)
    if t == datetime.datetime:
        res = datetime.datetime.strftime(param, '%Y-%m-%d %H:%M:%S')
    if t == datetime.date:
        res = datetime.datetime.strftime(param, '%Y-%m-%d')
    if t == time:
        res = time.strftime("%Y-%m-%d %H:%M:%S", param)
    return res


def if_empty_give_now_date(param=''):
    '''
    @ desc 如果值为空 就赋默认值 否则不做操作
    @ param param 要验证的值
    '''
    # 可否使用如下代码
    '''
    if not param:
      return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return param
    '''
    if not param:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    else:
        return param


def get_params(req):
    '''
    @ desc package request params according to request method
    @ param reqeust
    @ param_type request
    @ return_type dict
    '''
    params = {}
    if req.method.upper() in CONS.DANGER_REQ:
        params = req.args.to_dict()
    if req.method.upper() in CONS.SAFE_REQ:
        if not req.blueprint == 'upload':
            if req.data:
                params = json.loads(req.data.decode('UTF-8'))
        else:
            params = dict(file='图片 可能是集合 可能是单文件 emmm 需要重新写逻辑')
    return params


def get_wechat_params(req):
    '''
    @ desc package request params according to request method
    @ param reqeust
    @ param_type request
    @ return_type dict
    '''
    params = {}
    if req.method.upper() in CONS.DANGER_REQ:
        params = req.args.to_dict()
    if req.method.upper() in CONS.SAFE_REQ:
        params = req.form.to_dict()
    return params


def get_file(req):
    '''
    @ desc: get file from request
    @ info: judged whether this is multiple files
            or single file by according to parameter
            from the request
    @ param: request
    @ return: file
    @ author: wxyy
    '''
    file = req.files.get('file')
    if file:
        return [file]
    files = req.files.getlist('files')
    return files


def assign_post_fields(item):
    '''
    @ desc assign common fields eg: create_date/udpate_date/is_delete
    @ param dict to be handled
    @ param_type dict
    @ return_type dict
    '''
    if not item.get(CONS.CREATEDATE):
        item.update({CONS.CREATEDATE: if_empty_give_now_date()})
    if not item.get(CONS.UPDATEDATE):
        item.update({CONS.UPDATEDATE: if_empty_give_now_date()})
    if not item.get(CONS.ISDELETE):
        item.update({CONS.ISDELETE: 0})
    return item


def assign_put_fields(item):
    '''
    @ desc assign save fields eg: update_date
    @ param dict to be handled
    @ param_type dict
    @ return_type dict
    '''
    item.update({CONS.UPDATEDATE: if_empty_give_now_date()})
    return item


def assign_delete_fields(item):
    '''
    @ desc assign save fields eg: update_date/is_delete
    @ param dict to be handled
    @ param_type dict
    @ return_type dict
    '''
    item.update({CONS.UPDATEDATE: if_empty_give_now_date()})
    item.update({CONS.ISDELETE: -1})
    return item


def convert_type(v, t):
    '''
    @ desc: conver type of param to other type
    @ param: param value, param type
    @ return: result of convert or inial value
    @ author: wxyy
    '''
    if t in [datetime.datetime, datetime.date, time]:
        return convert_date(v)
    return v


def serialization_to_dict(o, l):
    # { key: getattr(self, str(value)) for key, value in ModeReSchema().items() }
    '''
    @ desc: serialization python object to dict
    @ param: python obejct, list of serialization dict
    @ param eg: User(), [{"updateDate", "update_date"}, {"createDate", "create_date"}]
    @ return: dict of serialization
    @ author: wxyy
    '''
    res = dict()
    for k, v in l:
        val = getattr(o, str(v))
        val_type = type(val)
        val_res = convert_type(val, val_type)
        res[k] = val_res
    return res


def get_fields(param):
    '''
    @ desc: get dict of custome attributes (comments enhance readability)
    @ param: Model from dto
    @ return: list of attributes
    @ author: wxyy
    '''
    # ----- original code -----
    # res = list()
    # for k in Mode.__dict__.keys():
    #     flag1 = not hasattr(getattr(Mode, k), '__call__')
    #     flag2 = not k in ['_sa_class_manager']
    #     flag3 = '__' not in k
    #     if flag1 & flag2 & flag3:
    #         res.append(k)
    # return res
    # ----- original code -----
    # ----- upgrade code -----
    return [k for k in param.__dict__.keys() if (not hasattr(getattr(param, k), '__call__')) & (k not in ['_sa_class_manager', 'password']) & ('__' not in k)]
    # ----- upgrade code -----


def convert_to_Camel_Case(param):
    '''
    @ desc: convert fields from model to Camel-Case
    @ param: fields from model
    @ return: list of fields convered
    @ author: wxyy
    '''
    def process_fields(o):
        '''
        @ desc: process every fields from model fields list
        @ param: string
        @ return: string that converted
        @ author: wxyy
        '''
        list = o.split('_')
        if len(list) > 1:
            cap_list = [v.capitalize() for v in list[1:]]
            o = list[0] + ''.join(cap_list)
        return o

    return [process_fields(o) for o in param]


def format_fields(o, l):
    '''
    @ desc: convert param from user to dto fields and filter parameter not able
    @ param: dict of parameter
    @ return: dict of parameter
    @ author: wxyy
    '''
    # convert_param = dict()
    # for key, value in param.items():
    #     if not param.get(key) == None:
    #         convert_param[value] = param.get(key)
    # return convert_param
    return {v: o.get(k) for k, v in l.items() if not o.get(k) == None}

def pack_params(req):
    url_params = req.args.to_dict()
    form_params = req.data and json.loads(req.data.decode('UTF-8')) or dict()
    params = dict(url_params, **form_params)
    return params
