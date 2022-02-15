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
