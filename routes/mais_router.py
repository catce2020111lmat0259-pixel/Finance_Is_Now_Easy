from flask import Flask
from controllers.mais import mais_controller


def adicionar_rotas(app: Flask):
    app.add_url_rule(rule="/fine/mais", endpoint="mais", view_func=mais_controller.mais_opcoes, methods=["GET"])