from src.model import Balance
from sqlalchemy import and_

DEFAULT_CONDITION = [Balance.is_delete >= 0]
LAST_CONDITION = Balance.create_date.desc()

def BALANCE_EACH_TOTAL_CONDITION(userId, type):
  con1 = Balance.user_id == userId
  con2 = Balance.is_delete >= 0
  con3 = Balance.type == type
  return and_(con1, con2, con3)