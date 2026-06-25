from flask import render_template, redirect, url_for, session, request
from datetime import datetime

from models.receitas.receitas_model import Receita
from models.despesas.despesas_model import Despesa
from models.database import db


def formatar_dia(data):
    hoje = datetime.today().date()

    ontem = hoje.replace(day=hoje.day - 1) if hoje.day > 1 else None

    dias_semana = {
        0: "Segunda",
        1: "Terça",
        2: "Quarta",
        3: "Quinta",
        4: "Sexta",
        5: "Sábado",
        6: "Domingo"
    }

    if data == hoje:
        return "Hoje"

    if ontem and data == ontem:
        return "Ontem"

    return f"{dias_semana[data.weekday()]}, {data.day:02d}"


def listar_transacoes():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    usuario_id = session["usuario_id"]

    busca = request.args.get("busca", "").strip()

    mes = request.args.get("mes", type=int)
    ano = request.args.get("ano", type=int)

    hoje = datetime.today()

    if not mes:
        mes = hoje.month

    if not ano:
        ano = hoje.year

    receitas = Receita.query.filter_by(usuario_id=usuario_id).filter(
        db.extract("month", Receita.data) == mes,
        db.extract("year", Receita.data) == ano
    ).all()

    despesas = Despesa.query.filter_by(usuario_id=usuario_id).filter(
        db.extract("month", Despesa.data) == mes,
        db.extract("year", Despesa.data) == ano
    ).all()

    transacoes = []

    for receita in receitas:
        transacoes.append({
            "id": receita.id,
            "tipo": "receita",
            "categoria": receita.categoria.nome,
            "descricao": receita.descricao,
            "valor": receita.valor,
            "data": receita.data,
            "status": "Recebido" if receita.recebido else "Não recebido"
        })

    for despesa in despesas:
        transacoes.append({
            "id": despesa.id,
            "tipo": "despesa",
            "categoria": despesa.categoria.nome,
            "descricao": despesa.descricao,
            "valor": despesa.valor,
            "data": despesa.data,
            "status": "Pago" if despesa.pago else "Pendente"
        })

    if busca:
        transacoes = [
            transacao for transacao in transacoes
            if busca.lower() in transacao["categoria"].lower()
            or busca.lower() in (transacao["descricao"] or "").lower()
            or busca.lower() in transacao["tipo"].lower()
            or busca.lower() in transacao["status"].lower()
        ]

    transacoes = sorted(transacoes, key=lambda item: item["data"])

    transacoes_por_dia = {}

    for transacao in transacoes:
        titulo_dia = formatar_dia(transacao["data"])

        if titulo_dia not in transacoes_por_dia:
            transacoes_por_dia[titulo_dia] = []

        transacoes_por_dia[titulo_dia].append(transacao)

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

    total_receitas = sum(r.valor for r in receitas)
    total_despesas = sum(d.valor for d in despesas)

    total_recebido = sum(r.valor for r in receitas if r.recebido)
    total_pago = sum(d.valor for d in despesas if d.pago)

    saldo_atual = total_recebido - total_pago
    resumo_mensal = total_receitas - total_despesas

    return render_template("transacoes/form-listar-transacoes.html", context={
        "transacoes_por_dia": transacoes_por_dia,
        "nome_mes": meses[mes],
        "mes": mes,
        "ano": ano,
        "mes_anterior": mes_anterior,
        "ano_anterior": ano_anterior,
        "mes_proximo": mes_proximo,
        "ano_proximo": ano_proximo,
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo_atual": saldo_atual,
        "resumo_mensal": resumo_mensal,
        "busca": busca
    })