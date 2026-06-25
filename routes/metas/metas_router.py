from flask import Flask
from controllers.metas import metas_controller

def adicionar_rotas(app: Flask):
    app.add_url_rule(rule="/fine/metas/criar", endpoint="criar_meta", view_func=metas_controller.criar_meta, methods=["GET"])
    app.add_url_rule(rule="/fine/metas/salvar", endpoint="salvar_meta", view_func=metas_controller.salvar_meta, methods=["POST"])
    app.add_url_rule(rule="/fine/metas/menu", endpoint="listar_metas", view_func=metas_controller.listar_metas, methods=["GET"])
    app.add_url_rule(rule="/fine/metas/editar/<int:id>", endpoint="editar_meta", view_func=metas_controller.editar_meta, methods=["GET", "POST"])
    app.add_url_rule(rule="/fine/metas/excluir/confirmar/<int:id>", endpoint="confirmar_exclusao_meta", view_func=metas_controller.confirmar_exclusao_meta, methods=["POST"])
    app.add_url_rule(rule="/fine/metas/fixar/<int:id>", endpoint="fixar_meta", view_func=metas_controller.fixar_meta, methods=["GET"])