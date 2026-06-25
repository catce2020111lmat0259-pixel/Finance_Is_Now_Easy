from flask import Flask
from controllers.transacoes import transacoes_controller


def adicionar_rotas(app: Flask):
    app.add_url_rule(rule="/fine/transacoes/listar",endpoint="listar_transacoes",view_func=transacoes_controller.listar_transacoes,methods=["GET"])