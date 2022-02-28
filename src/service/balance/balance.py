from marshmallow import fields
from src.model import Balance, BalanceSchema, BalanceReSchema
from src.common import BALANCE_FIELDS, BALANCE_CONDITION
from src.utils import db, util


def balance_list():
    # param = util.format_fields(BalanceReSchema())
    balance_schema = BalanceSchema()
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
    