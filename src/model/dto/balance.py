from src.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from src.utils import util


class Balance(db.Model):
    # 定义表名
    __tablename__ = 'balance'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer)
    amount = db.Column(db.DECIMAL)
    balance = db.Column(db.DECIMAL)
    create_date = db.Column(db.DateTime(10))
    update_date = db.Column(db.DateTime(10))
    is_delete = db.Column(db.Integer)

    def get_schema(self):
        return util.serialization_to_dict(self, BalanceReSchema().items())

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class BalanceSchema(ModelSchema):
    class Meta:
        model = Balance
        # sqla_session = db.session

    id = fields.Number()
    type = fields.Number()
    amount = fields.Number()
    balance = fields.Number()
    createDate = fields.String()
    updateDate = fields.String()
    isDelete = fields.Number()


def BalanceReSchema():
    values = util.get_fields(Balance)
    keys = util.convert_to_Camel_Case(values)
    return dict(zip(keys, values))