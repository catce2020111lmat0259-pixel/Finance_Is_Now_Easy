from flask import Flask
from controllers.receitas import receitas_controller

def adicionar_rotas(app: Flask):
    app.add_url_rule("/fine/receitas/criar", "criar_receita", receitas_controller.criar_receita, methods=["GET"])
    app.add_url_rule("/fine/receitas/salvar", "salvar_receita", receitas_controller.salvar_receita, methods=["POST"])
    app.add_url_rule("/fine/receitas/menu", "listar_receitas", receitas_controller.listar_receitas, methods=["GET"])
    app.add_url_rule("/fine/receitas/editar/<int:id>", "editar_receita", receitas_controller.editar_receita, methods=["GET", "POST"])
    app.add_url_rule("/fine/receitas/excluir/confirmar/<int:id>", "confirmar_exclusao_receita", receitas_controller.confirmar_exclusao_receita, methods=["POST"])