from sqlalchemy import func
from src.model import Balance

BALANCE_LIST = [
  Balance.id.label('id'),
  Balance.type.label('type'),
  Balance.amount.label('amount'),
  Balance.balance.label('balance'),
  Balance.create_date.label('createDate'),
  Balance.update_date.label('updateDate'),
  Balance.is_delete.label('isDelete')
]

BALANCE_EACH_TOTAL = [func.sum(Balance.amount).label('sum')]
