from flask import Flask
from controllers.categorias import categorias_controller

def adicionar_rotas(app: Flask):
    app.add_url_rule(rule="/fine/categorias/criar", endpoint="criar_categoria", view_func=categorias_controller.criar_categoria, methods=["GET"])
    app.add_url_rule(rule="/fine/categorias/salvar", endpoint="salvar_categoria", view_func=categorias_controller.salvar_categoria, methods=["POST"])
    app.add_url_rule(rule="/fine/categorias/menu", endpoint="listar_categorias", view_func=categorias_controller.listar_categorias, methods=["GET"])
    app.add_url_rule(rule="/fine/categorias/editar/<int:id>", endpoint="editar_categoria", view_func=categorias_controller.editar_categoria, methods=["GET", "POST"])
    app.add_url_rule(rule="/fine/categorias/excluir/confirmar/<int:id>", endpoint="confirmar_exclusao_categoria", view_func=categorias_controller.confirmar_exclusao_categoria, methods=["GET", "POST"])