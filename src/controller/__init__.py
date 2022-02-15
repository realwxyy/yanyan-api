from src.controller.test.test import t
from src.controller.balance.balance import balance_controller

def resgister_test(app):
    app.register_blueprint(t)


def register_all_blueprint(app):
    '''
    @ desc: register all blueprint
    @ param: app
    @ return: not needed
    @ author: wxyy
    '''
    app.register_blueprint(t)
    app.register_blueprint(balance_controller)
