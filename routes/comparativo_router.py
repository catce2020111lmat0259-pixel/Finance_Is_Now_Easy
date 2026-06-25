from flask import Flask
from controllers.comparativo import comparativo_controller

def adicionar_rotas(app: Flask):
    app.add_url_rule(rule="/fine/comparativo", endpoint="comparativo_mensal", view_func=comparativo_controller.comparativo_mensal, methods=["GET"])