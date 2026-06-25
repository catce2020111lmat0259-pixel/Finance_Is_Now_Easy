from flask import Flask

from controllers import index_controller

def adicionar_rotas(app: Flask):
    app.add_url_rule(rule="/", endpoint="home", view_func=index_controller.home, methods=["GET"])
