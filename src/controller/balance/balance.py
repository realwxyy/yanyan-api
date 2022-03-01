from flask import Blueprint, make_response, jsonify, request
from src.utils import util, resp
from src.service import balance_service
import decimal

balance_controller = Blueprint('balance', __name__, url_prefix='/balance')

@balance_controller.route('/get-balance', methods=['get'])
def get_balance():
  res = balance_service.get_last()
  if not res.get('code') == 0:
    return resp.resp_fail(message=res.get('message'))
  res.pop('code')
  return resp.resp_succ(res.get('data'), message='查询成功')

@balance_controller.route('/get-balances', methods=['get'])
def get_balances():
  res = balance_service.balance_list()
  if not res.get('code') == 0:
      return resp.resp_fail(message=res.get('message'))
  res.pop('code')
  return resp.resp_succ(res.get('list'), message='查询成功')

@balance_controller.route('/get-each-total', methods=['get'])
def get_each_total():
  res = balance_service.get_each_total()
  if not res.get('code') == 0:
      return resp.resp_fail(message=res.get('message'))
  res.pop('code')
  return resp.resp_succ(res.get('data'), message='查询成功')

@balance_controller.route('/save', methods=['post'])
def save():
    '''
    @ desc: add repository file menu
    @ param: request
    @ return: resp
    @ author: wxyy
    '''
    param = util.pack_params(request)
    valid = util.dict_not_empty(param, ['userId', 'type', 'amount'])
    balance = 0
    if not valid.get('code') == 0:
      return resp.resp_fail(message=valid.get('msg'))
    last_res = balance_service.get_last()
    if not last_res.get('code') == 0:
      return resp.resp_fail(message=last_res.get('message'))
    last_balance = last_res.get('data').get('balance')
    last_balance = decimal.Decimal(last_balance if last_balance else 0)
    type = param.get('type')
    amount = param.get('amount')
    if (type):
      amount = decimal.Decimal(amount)
    else:
      amount = -decimal.Decimal(amount)
    balance = last_balance + amount
    param.update({ 'balance': balance })
    param = util.assign_post_fields(param)
    res = balance_service.save(param)
    if not res.get('code') == 0:
      return resp.resp_fail(message=res.get('message'))
    res.pop('code')
    return resp.resp_succ(res.get('data'), message='添加成功')
