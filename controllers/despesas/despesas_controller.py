from flask import render_template, request, redirect, url_for, session
from datetime import datetime, date
from models.despesas.despesas_model import Despesa
from models.categorias.categorias_model import Categoria

from controllers.categorias.categorias_controller import criar_categorias_padrao

from models.database import db


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

def criar_despesa():
    if "usuario_id" not in session:
        return redirect(url_for("login"))
    
    criar_categorias_padrao(session["usuario_id"])

    categorias = Categoria.query.filter_by(usuario_id=session["usuario_id"], tipo="despesa").all()

    return render_template("despesas/form-criar-despesa.html", context={
        "categorias": categorias
        })


def salvar_despesa():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    valor = request.form.get("valor")
    descricao = request.form.get("descricao")
    data = request.form.get("data")
    pago = request.form.get("pago")
    categoria_id = request.form.get("categoria_id")

    errors = []

    if not valor:
        errors.append("O valor da despesa é obrigatório.")
    else:
        try:
            valor = valor.replace(".", "").replace(",", ".")
            valor = float(valor)
        except ValueError:
            errors.append("Valor da despesa inválido.")

    if not data:
        errors.append("A data da despesa é obrigatória.")
    else:
        try:
            data = datetime.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            errors.append("Data inválida.")

    if categoria_id:
        categoria_id = int(categoria_id)

    despesa = Despesa(
        valor=valor if not isinstance(valor, str) else 0,
        descricao=descricao,
        data=data if data else None,
        pago=True if pago == "on" else False,
        categoria_id=categoria_id if categoria_id else None,
        usuario_id=session["usuario_id"]
    )

    errors += despesa.validate()

    categorias = Categoria.query.filter_by(
        usuario_id=session["usuario_id"],
        tipo="despesa"
    ).all()

    if not errors:
        db.session.add(despesa)
        db.session.commit()

        return redirect(url_for("listar_despesas"))

    return render_template(
        "despesas/form-criar-despesa.html",
        context={
            "despesa": despesa,
            "categorias": categorias,
            "erros": errors
        }
    )

def listar_despesas():
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

    query = Despesa.query.filter_by(usuario_id=session["usuario_id"])
    query = query.filter(
        db.extract("month", Despesa.data) == mes,
        db.extract("year", Despesa.data) == ano
    )
    
    if busca:
        query = query.join(Categoria).filter(
            (Despesa.descricao.ilike(f"%{busca}%")) |
            (Categoria.nome.ilike(f"%{busca}%"))
        )

    if categoria_id:
        query = query.filter(Despesa.categoria_id == int(categoria_id))

    if status == "pago":
        query = query.filter(Despesa.pago == True)

    elif status == "pendente":
        query = query.filter(Despesa.pago == False)

    if data_inicio:
        data_inicio_convertida = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        query = query.filter(Despesa.data >= data_inicio_convertida)

    if data_fim:
        data_fim_convertida = datetime.strptime(data_fim, "%Y-%m-%d").date()
        query = query.filter(Despesa.data <= data_fim_convertida)
        
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

    despesas = query.order_by(Despesa.data.asc()).all()

    categorias = Categoria.query.filter_by(
        usuario_id=session["usuario_id"],
        tipo="despesa"
    ).all()

    total_pendente = 0
    total_pago = 0
    despesas_por_dia = {}

    for despesa in despesas:
        if despesa.pago:
            total_pago += despesa.valor
        else:
            total_pendente += despesa.valor

        titulo_dia = formatar_dia(despesa.data)

        if titulo_dia not in despesas_por_dia:
            despesas_por_dia[titulo_dia] = []

        despesas_por_dia[titulo_dia].append(despesa)

    return render_template("despesas/form-listar-despesa.html", context={
        "despesas_por_dia": despesas_por_dia,
        "total_pendente": total_pendente,
        "total_pago": total_pago,
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
    
def editar_despesa(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    despesa = Despesa.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()

    if not despesa:
        return redirect(url_for("listar_despesas"))

    categorias = Categoria.query.filter_by(usuario_id=session["usuario_id"], tipo="despesa").all()

    if request.method == "POST":
        valor = request.form.get("valor")
        descricao = request.form.get("descricao")
        data = request.form.get("data")
        pago = request.form.get("pago")
        categoria_id = request.form.get("categoria_id")

        errors = []

        if not valor:
            errors.append("O valor da despesa é obrigatório.")
        else:
            try:
                valor = valor.replace(".", "").replace(",", ".")
                valor = float(valor)
            except ValueError:
                errors.append("Valor da despesa inválido.")

        if not data:
            errors.append("A data da despesa é obrigatória.")
        else:
            try:
                data = datetime.strptime(data, "%Y-%m-%d").date()
            except ValueError:
                errors.append("Data inválida.")

        if categoria_id:
            categoria_id = int(categoria_id)

        despesa.valor = valor if not isinstance(valor, str) else 0
        despesa.descricao = descricao
        despesa.data = data if data else None
        despesa.pago = True if pago == "on" else False
        despesa.categoria_id = categoria_id if categoria_id else None

        errors += despesa.validate()

        if not errors:
            db.session.commit()
            return redirect(url_for("listar_despesas"))

        return render_template("despesas/form-editar-despesa.html", context={
            "despesa": despesa,
            "categorias": categorias,
            "erros": errors
        })

    return render_template("despesas/form-editar-despesa.html", context={
        "despesa": despesa,
        "categorias": categorias
    })

def confirmar_exclusao_despesa(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    despesa = Despesa.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()

    if not despesa:
        return redirect(url_for("listar_despesas"))

    if request.method == "POST":
        confirmacao = request.form.get("confirmar-exclusao")

        if confirmacao == "Sim":
            db.session.delete(despesa)
            db.session.commit()

    return redirect(url_for("listar_despesas"))