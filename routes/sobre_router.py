from flask import Flask
from controllers.sobre import sobre_controller

def adicionar_rotas(app: Flask):
    app.add_url_rule(rule="/fine/sobre", endpoint="sobre", view_func=sobre_controller.sobre, methods=["GET"])