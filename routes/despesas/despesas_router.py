from flask import Flask, app
from controllers.despesas import despesas_controller

def adicionar_rotas(app: Flask):
    app.add_url_rule("/fine/despesas/criar", "criar_despesa", despesas_controller.criar_despesa, methods=["GET"])
    app.add_url_rule("/fine/despesas/salvar", "salvar_despesa", despesas_controller.salvar_despesa, methods=["POST"])
    app.add_url_rule("/fine/despesas/menu", "listar_despesas", despesas_controller.listar_despesas, methods=["GET"])
    app.add_url_rule("/fine/despesas/editar/<int:id>", "editar_despesa", despesas_controller.editar_despesa, methods=["GET", "POST"])
    app.add_url_rule("/fine/despesas/excluir/confirmar/<int:id>", "confirmar_exclusao_despesa", despesas_controller.confirmar_exclusao_despesa, methods=["POST"])