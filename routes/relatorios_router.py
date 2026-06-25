from flask import Flask
from controllers.relatorios import relatorios_controller


def adicionar_rotas(app: Flask):
    app.add_url_rule(rule="/fine/relatorios/exportar", endpoint="gerar_relatorio", view_func=relatorios_controller.exportar_relatorio, methods=["GET"])