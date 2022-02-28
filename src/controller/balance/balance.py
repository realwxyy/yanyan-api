from flask import Blueprint, make_response, jsonify, request
from src.utils import util, resp
from src.service import balance_service

balance_controller = Blueprint('balance', __name__, url_prefix='/balance')


@balance_controller.route('/get-balances', methods=['get'])
def get_balances():
  res = balance_service.balance_list()
  if not res.get('code') == 0:
      return resp.resp_fail(message=res.get('message'))
  res.pop('code')
  return resp.resp_succ(res.get('list'), message='查询成功')

@balance_controller.route('/get-balance', methods=['get'])
def t1():
  return 'welocome to /test/t1'

@balance_controller.route('/save', methods=['post'])
def save():
    '''
    @ desc: add repository file menu
    @ param: request
    @ return: resp
    @ author: wxyy
    '''
    param = util.pack_params(request)
    valid = util.dict_not_empty(param, ['type', 'amount', 'balance'])
    if not valid.get('code') == 0:
        return resp.resp_fail(message=valid.get('msg'))
    param = util.assign_post_fields(param)
    res = balance_service.save(param)
    print(res)
    if not res.get('code') == 0:
        return resp.resp_fail(message=res.get('message'))
    res.pop('code')
    return resp.resp_succ(res, message='添加成功')
