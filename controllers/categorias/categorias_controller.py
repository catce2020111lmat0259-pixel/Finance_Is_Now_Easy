from flask import render_template, request, redirect, url_for, session
from models.categorias.categorias_model import Categoria
from models.database import db


def criar_categorias_padrao(usuario_id):
    categorias_padrao = [

        # RECEITAS
        {"nome": "Bonificação", "descricao": "Prêmios e recompensas", "tipo": "receita", "cor": "#00a54a"},
        {"nome": "Empréstimo", "descricao": "Valores recebidos por empréstimo", "tipo": "receita", "cor": "#d7fd2c"},
        {"nome": "Investimento", "descricao": "Rendimentos e dividendos", "tipo": "receita", "cor": "#7c3fcc"},
        {"nome": "Outros", "descricao": "Outras entradas financeiras", "tipo": "receita", "cor": "#999999"},
        {"nome": "Pix", "descricao": "Recebimentos via Pix", "tipo": "receita", "cor": "#d40655"},
        {"nome": "Renda Extra", "descricao": "Trabalhos e ganhos adicionais", "tipo": "receita", "cor": "#00a54a"},
        {"nome": "Salário", "descricao": "Remuneração principal", "tipo": "receita", "cor": "#00a54a"},
        {"nome": "Transferência Bancária", "descricao": "Recebimentos por transferência", "tipo": "receita", "cor": "#00bcdd"},

        # DESPESAS
        {"nome": "Alimentação", "descricao": "Refeições e alimentação em geral", "tipo": "despesa", "cor": "#ef4444"},
        {"nome": "Assinaturas", "descricao": "Serviços recorrentes e assinaturas", "tipo": "despesa", "cor": "#8400ff"},
        {"nome": "Casa", "descricao": "Moradia, aluguel e contas domésticas", "tipo": "despesa", "cor": "#f97316"},
        {"nome": "Compras", "descricao": "Aquisição de produtos diversos", "tipo": "despesa", "cor": "#8400ff"},
        {"nome": "Educação", "descricao": "Cursos, faculdade e estudos", "tipo": "despesa", "cor": "#aa24d3"},
        {"nome": "Lazer", "descricao": "Entretenimento e diversão", "tipo": "despesa", "cor": "#8400ff"},
        {"nome": "Operação Bancária", "descricao": "Taxas e tarifas bancárias", "tipo": "despesa", "cor": "#1c60c0"},
        {"nome": "Outros", "descricao": "Outras despesas", "tipo": "despesa", "cor": "#999999"},
        {"nome": "Pix", "descricao": "Pagamentos via Pix", "tipo": "despesa", "cor": "#00bcdd"},
        {"nome": "Saúde", "descricao": "Consultas, exames e medicamentos", "tipo": "despesa", "cor": "#dc2626"},
        {"nome": "Supermercado", "descricao": "Compras de mercado", "tipo": "despesa", "cor": "#f59e0b"},
        {"nome": "Transporte", "descricao": "Combustível, ônibus e aplicativos", "tipo": "despesa", "cor": "#00bcdd"},
        {"nome": "Viagem", "descricao": "Passagens, hospedagem e turismo", "tipo": "despesa", "cor": "#1f22ff"}
    ]

    for item in categorias_padrao:
        categoria_existente = Categoria.query.filter_by(
            nome=item["nome"],
            tipo=item["tipo"],
            usuario_id=usuario_id
        ).first()

        if not categoria_existente:
            categoria = Categoria(
                nome=item["nome"],
                descricao=item["descricao"],
                tipo=item["tipo"],
                cor=item["cor"],
                usuario_id=usuario_id,
                padrao=True
            )

            db.session.add(categoria)

    db.session.commit()

def criar_categoria():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    
    criar_categorias_padrao(session["usuario_id"])

    return render_template("categorias/form-criar-categoria.html")


def salvar_categoria():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    tipo = request.form.get("tipo")
    cor = request.form.get("cor")

    categoria = Categoria(
        nome=nome,
        descricao=descricao,
        tipo=tipo,
        cor=cor,
        usuario_id=session["usuario_id"]
    )

    errors = categoria.validate()

    if not errors:
        db.session.add(categoria)
        db.session.commit()

        return redirect(url_for("listar_categorias"))

    return render_template("categorias/form-criar-categoria.html", context={
        "categoria": categoria,
        "erros": errors
    })
    
def listar_categorias():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    criar_categorias_padrao(session["usuario_id"])

    busca = request.args.get("busca", "").strip()
    tipo = request.args.get("tipo", "").strip()

    query = Categoria.query.filter_by(usuario_id=session["usuario_id"])

    if busca:
        query = query.filter(
            (Categoria.nome.ilike(f"%{busca}%")) |
            (Categoria.descricao.ilike(f"%{busca}%"))
        )

    if tipo in ["receita", "despesa"]:
        query = query.filter(Categoria.tipo == tipo)

    categorias = query.order_by(Categoria.tipo.asc(), Categoria.nome.asc()).all()

    receitas = []
    despesas = []

    for categoria in categorias:
        if categoria.tipo == "receita":
            receitas.append(categoria)
        elif categoria.tipo == "despesa":
            despesas.append(categoria)

    return render_template("categorias/form-listar-categoria.html", context={
        "receitas": receitas,
        "despesas": despesas,
        "busca": busca,
        "tipo": tipo
    })

def editar_categoria(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    categoria = Categoria.query.filter_by(
        id=id,
        usuario_id=session["usuario_id"]
    ).first()

    if not categoria:
        return redirect(url_for("listar_categorias"))

    if request.method == "POST":
        cor = request.form.get("cor")

        if categoria.padrao:
            categoria.cor = cor
        else:
            categoria.nome = request.form.get("nome")
            categoria.descricao = request.form.get("descricao")
            categoria.tipo = request.form.get("tipo")
            categoria.cor = cor

        errors = categoria.validate()

        if not errors:
            db.session.commit()
            return redirect(url_for("listar_categorias"))

        return render_template("categorias/form-editar-categoria.html", context={
            "categoria": categoria,
            "erros": errors
        })

    return render_template("categorias/form-editar-categoria.html", context={
        "categoria": categoria
    })

def confirmar_exclusao_categoria(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    categoria = Categoria.query.filter_by(
        id=id,
        usuario_id=session["usuario_id"]
    ).first()

    if not categoria:
        return redirect(url_for("listar_categorias"))

    if categoria.padrao:
        return redirect(url_for("listar_categorias"))

    if request.method == "POST":
        confirmacao = request.form.get("confirmar-exclusao")

        if confirmacao == "Sim":
            db.session.delete(categoria)
            db.session.commit()

    return redirect(url_for("listar_categorias"))