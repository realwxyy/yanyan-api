from marshmallow import fields
from src.model import Balance, BalanceSchema, BalanceReSchema
from src.common import BALANCE_FIELDS, BALANCE_CONDITION
from src.utils import db, util

def balance_list():
  # param = util.format_fields(BalanceReSchema())
  # balance_schema = BalanceSchema()
  query = BALANCE_FIELDS.BALANCE_LIST
  con = BALANCE_CONDITION.DEFAULT_CONDITION
  try:
    sql_res = db.session.query(*query).filter(*con)
    data = sql_res.all()
    balance_schema = BalanceSchema(many=True)
    balances = balance_schema.dump(data)
    return dict(code=0, list=balances)
  except Exception as e:
    return dict(code=-1, message='其他错误: ' + str(e))

def save(param):
  try:
    param = util.format_fields(param, BalanceReSchema())
    balance_schema = BalanceSchema()
    balance = balance_schema.load(param, session=db.session)
    res = balance.save().get_schema()
    return dict(code=0, data=res)
  except Exception as e:
    return dict(code=-1, message='其他错误: ' + str(e))

def get_last():
  balance_schema = BalanceSchema()
  query = BALANCE_FIELDS.BALANCE_LIST
  filter_con = BALANCE_CONDITION.DEFAULT_CONDITION
  order_con = BALANCE_CONDITION.LAST_CONDITION
  try:
    sql_res = db.session.query(*query).order_by(order_con).filter(*filter_con)
    data = sql_res.first()
    balance_schema = BalanceSchema()
    balance = balance_schema.dump(data)
    return dict(code=0, data=balance)
  except Exception as e:
    return dict(code=-1, message='其他错误: ' + str(e))

def get_each_total():
  query = BALANCE_FIELDS.BALANCE_EACH_TOTAL
  filter_girl_in_con = BALANCE_CONDITION.BALANCE_EACH_TOTAL_CONDITION(1, 1)
  filter_boy_in_con = BALANCE_CONDITION.BALANCE_EACH_TOTAL_CONDITION(2, 1)
  try:
    boy_in_sql_res = db.session.query(*query).filter(filter_girl_in_con).first()
    girl_in_sql_res = db.session.query(*query).filter(filter_boy_in_con).first()
    boy_in = boy_in_sql_res.sum
    girl_in = girl_in_sql_res.sum
    data = dict(boyIn=boy_in, girlIn=girl_in)
    return dict(code=0, data=data)
  except Exception as e:
    return dict(code=-1, message='其他错误: ' + str(e)) 