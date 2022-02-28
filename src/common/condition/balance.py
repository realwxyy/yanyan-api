from src.model import Balance

DEFAULT_CONDITION = [Balance.is_delete >= 0]
LAST_CONDITION = Balance.create_date.desc()