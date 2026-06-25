from flask import Flask

from dotenv import load_dotenv
import os

from models.database import db

from models.login.usuario_model import Usuario
from models.categorias.categorias_model import Categoria
from models.despesas.despesas_model import Despesa
from models.metas.metas_model import Meta
from models.receitas.receitas_model import Receita

from routes import index_router
from routes import comparativo_router
from routes import mais_router
from routes import relatorios_router
from routes import sobre_router
from routes import transacoes_router
from routes.login import usuario_router
from routes.categorias import categorias_router
from routes.despesas import despesas_router
from routes.metas import metas_router
from routes.receitas import receitas_router

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = "fine_secret_key_2026"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

# inicializa banco
db.init_app(app)

# rotas
index_router.adicionar_rotas(app)
comparativo_router.adicionar_rotas(app)
mais_router.adicionar_rotas(app)
relatorios_router.adicionar_rotas(app)
sobre_router.adicionar_rotas(app)
transacoes_router.adicionar_rotas(app)
metas_router.adicionar_rotas(app)
usuario_router.adicionar_rotas(app)
categorias_router.adicionar_rotas(app)
despesas_router.adicionar_rotas(app)
receitas_router.adicionar_rotas(app)

# cria tabelas automaticamente (dev/local)
with app.app_context():
    db.create_all()