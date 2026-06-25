from flask import render_template, request, redirect, url_for, session
from datetime import datetime, date
from models.receitas.receitas_model import Receita
from models.categorias.categorias_model import Categoria
from controllers.categorias.categorias_controller import criar_categorias_padrao
from models.database import db


def criar_receita():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    criar_categorias_padrao(session["usuario_id"])

    categorias = Categoria.query.filter_by(usuario_id=session["usuario_id"], tipo="receita").all()

    return render_template("receitas/form-criar-receita.html", context={
        "categorias": categorias
    })


def salvar_receita():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    valor = request.form.get("valor")
    descricao = request.form.get("descricao")
    data = request.form.get("data")
    recebido = request.form.get("recebido")
    categoria_id = request.form.get("categoria_id")

    errors = []

    if not valor:
        errors.append("O valor da receita é obrigatório.")
    else:
        try:
            valor = valor.replace(".", "").replace(",", ".")
            valor = float(valor)
        except ValueError:
            errors.append("Valor da receita inválido.")

    if not data:
        errors.append("A data da receita é obrigatória.")
    else:
        try:
            data = datetime.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            errors.append("Data inválida.")

    if categoria_id:
        categoria_id = int(categoria_id)

    receita = Receita(
        valor=valor if not isinstance(valor, str) else 0,
        descricao=descricao,
        data=data if data else None,
        recebido=True if recebido == "on" else False,
        categoria_id=categoria_id if categoria_id else None,
        usuario_id=session["usuario_id"]
    )

    errors += receita.validate()

    categorias = Categoria.query.filter_by(usuario_id=session["usuario_id"], tipo="receita").all()

    if not errors:
        db.session.add(receita)
        db.session.commit()

        return redirect(url_for("listar_receitas"))

    return render_template("receitas/form-criar-receita.html", context={
        "receita": receita,
        "categorias": categorias,
        "erros": errors
    })


def formatar_dia(data):
    hoje = date.today()

    if data == hoje:
        return "Hoje"

    if (hoje - data).days == 1:
        return "Ontem"

    dias_semana = [
        "Segunda",
        "Terça",
        "Quarta",
        "Quinta",
        "Sexta",
        "Sábado",
        "Domingo"
    ]

    return f"{dias_semana[data.weekday()]}, {data.day:02d}"

def listar_receitas():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    categoria_id = request.args.get("categoria_id")
    status = request.args.get("status")
    data_inicio = request.args.get("data_inicio")
    data_fim = request.args.get("data_fim")

    busca = request.args.get("busca", "").strip()

    mes = request.args.get("mes", type=int)
    ano = request.args.get("ano", type=int)
    hoje = datetime.today()

    if not mes:
        mes = hoje.month

    if not ano:
        ano = hoje.year

    query = Receita.query.filter_by(usuario_id=session["usuario_id"])

    query = query.filter(
        db.extract("month", Receita.data) == mes,
        db.extract("year", Receita.data) == ano
    )

    if busca:
        query = query.join(Categoria).filter(
            (Receita.descricao.ilike(f"%{busca}%")) |
            (Categoria.nome.ilike(f"%{busca}%"))
        )

    if categoria_id:
        query = query.filter(Receita.categoria_id == int(categoria_id))

    if status == "recebido":
        query = query.filter(Receita.recebido == True)

    elif status == "pendente":
        query = query.filter(Receita.recebido == False)

    if data_inicio:
        data_inicio_convertida = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        query = query.filter(Receita.data >= data_inicio_convertida)

    if data_fim:
        data_fim_convertida = datetime.strptime(data_fim, "%Y-%m-%d").date()
        query = query.filter(Receita.data <= data_fim_convertida)

    meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }

    nome_mes = meses[mes]

    mes_anterior = mes - 1
    ano_anterior = ano

    if mes_anterior == 0:
        mes_anterior = 12
        ano_anterior -= 1

    mes_proximo = mes + 1
    ano_proximo = ano

    if mes_proximo == 13:
        mes_proximo = 1
        ano_proximo += 1

    receitas = query.order_by(Receita.data.asc()).all()

    categorias = Categoria.query.filter_by(
        usuario_id=session["usuario_id"],
        tipo="receita"
    ).all()

    total_pendente = 0
    total_recebido = 0
    receitas_por_dia = {}

    for receita in receitas:
        if receita.recebido:
            total_recebido += receita.valor
        else:
            total_pendente += receita.valor

        titulo_dia = formatar_dia(receita.data)

        if titulo_dia not in receitas_por_dia:
            receitas_por_dia[titulo_dia] = []

        receitas_por_dia[titulo_dia].append(receita)

    return render_template("receitas/form-listar-receita.html", context={
        "receitas_por_dia": receitas_por_dia,
        "total_pendente": total_pendente,
        "total_recebido": total_recebido,
        "categorias": categorias,
        "categoria_id": categoria_id,
        "status": status,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "busca": busca,
        "mes": mes,
        "ano": ano,
        "nome_mes": nome_mes,
        "mes_anterior": mes_anterior,
        "ano_anterior": ano_anterior,
        "mes_proximo": mes_proximo,
        "ano_proximo": ano_proximo
    })
    
def editar_receita(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    receita = Receita.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()

    if not receita:
        return redirect(url_for("listar_receitas"))

    categorias = Categoria.query.filter_by(usuario_id=session["usuario_id"], tipo="receita").all()

    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        data = request.form.get("data")
        recebido = request.form.get("recebido")
        categoria_id = request.form.get("categoria_id")

        errors = []

        if not valor:
            errors.append("O valor da receita é obrigatório.")
        else:
            try:
                valor = valor.replace(".", "").replace(",", ".")
                valor = float(valor)
            except ValueError:
                errors.append("Valor da receita inválido.")

        if not data:
            errors.append("A data da receita é obrigatória.")
        else:
            try:
                data = datetime.strptime(data, "%Y-%m-%d").date()
            except ValueError:
                errors.append("Data inválida.")

        if categoria_id:
            categoria_id = int(categoria_id)

        receita.valor = valor if not isinstance(valor, str) else 0
        receita.descricao = descricao
        receita.data = data if data else None
        receita.recebido = True if recebido == "on" else False
        receita.categoria_id = categoria_id if categoria_id else None

        errors += receita.validate()

        if not errors:
            db.session.commit()
            return redirect(url_for("listar_receitas"))

        return render_template("receitas/form-editar-receita.html", context={
            "receita": receita,
            "categorias": categorias,
            "erros": errors
        })

    return render_template("receitas/form-editar-receita.html", context={
        "receita": receita,
        "categorias": categorias
    })

def confirmar_exclusao_receita(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    receita = Receita.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()

    if not receita:
        return redirect(url_for("listar_receitas"))

    if request.method == "POST":
        confirmacao = request.form.get("confirmar-exclusao")

        if confirmacao == "Sim":
            db.session.delete(receita)
            db.session.commit()

    return redirect(url_for("listar_receitas"))