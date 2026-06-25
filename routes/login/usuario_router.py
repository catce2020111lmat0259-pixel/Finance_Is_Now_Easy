from flask import Flask
from controllers.login import usuario_controller


def adicionar_rotas(app: Flask):
    app.add_url_rule(rule="/fine/usuarios/criar", endpoint="criar_usuario", view_func=usuario_controller.criar_usuario, methods=["GET"])
    app.add_url_rule(rule="/fine/usuarios/salvar", endpoint="salvar_usuario", view_func=usuario_controller.salvar_usuario, methods=["POST"])
    
    app.add_url_rule(rule="/fine/login", endpoint="login", view_func=usuario_controller.login, methods=["GET"])
    app.add_url_rule(rule="/fine/login/autenticar", endpoint="autenticar", view_func=usuario_controller.autenticar, methods=["POST"])
    app.add_url_rule(rule="/fine/login/logout", endpoint="logout", view_func=usuario_controller.logout, methods=["GET"])
    
    app.add_url_rule(rule="/fine/recuperacao/senha", endpoint="esqueci_senha", view_func=usuario_controller.esqueci_senha, methods=["GET"])
    app.add_url_rule(rule="/fine/recuperacao/senha/verificar", endpoint="verificar_recuperacao", view_func=usuario_controller.verificar_recuperacao, methods=["POST"])
    app.add_url_rule(rule="/fine/recuperacao/senha/nova", endpoint="salvar_nova_senha", view_func=usuario_controller.salvar_nova_senha, methods=["POST"])