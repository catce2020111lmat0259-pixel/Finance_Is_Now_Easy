from flask import render_template, redirect, url_for, session, request
from datetime import datetime

from models.database import db
from models.receitas.receitas_model import Receita
from models.despesas.despesas_model import Despesa


def comparativo_mensal():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    usuario_id = session["usuario_id"]

    ano = request.args.get("ano", type=int)

    if not ano:
        ano = datetime.today().year

    ano_anterior = ano - 1
    ano_proximo = ano + 1

    meses = [
        "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
        "Jul", "Ago", "Set", "Out", "Nov", "Dez"
    ]

    receitas_mes = []
    despesas_mes = []
    saldo_mes = []

    for mes in range(1, 13):

        total_receitas = db.session.query(
            db.func.coalesce(db.func.sum(Receita.valor), 0)
        ).filter(
            Receita.usuario_id == usuario_id,
            db.extract("month", Receita.data) == mes,
            db.extract("year", Receita.data) == ano
        ).scalar()

        total_despesas = db.session.query(
            db.func.coalesce(db.func.sum(Despesa.valor), 0)
        ).filter(
            Despesa.usuario_id == usuario_id,
            db.extract("month", Despesa.data) == mes,
            db.extract("year", Despesa.data) == ano
        ).scalar()

        total_receitas = float(total_receitas)
        total_despesas = float(total_despesas)
        saldo = total_receitas - total_despesas

        receitas_mes.append(total_receitas)
        despesas_mes.append(total_despesas)
        saldo_mes.append(saldo)

    total_receitas_ano = sum(receitas_mes)
    total_despesas_ano = sum(despesas_mes)
    saldo_ano = total_receitas_ano - total_despesas_ano

    return render_template(
        "comparativo/form-comparativo.html",
        context={
            "ano": ano,
            "ano_anterior": ano_anterior,
            "ano_proximo": ano_proximo,
            "meses": meses,
            "receitas": receitas_mes,
            "despesas": despesas_mes,
            "saldo": saldo_mes,
            "total_receitas_ano": total_receitas_ano,
            "total_despesas_ano": total_despesas_ano,
            "saldo_ano": saldo_ano
        }
    )