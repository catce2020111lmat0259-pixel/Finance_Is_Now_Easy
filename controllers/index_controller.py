from flask import render_template, redirect, request, url_for, session
from datetime import datetime

from models.receitas.receitas_model import Receita
from models.despesas.despesas_model import Despesa
from models.metas.metas_model import Meta
from models.database import db

def home():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    usuario_id = session["usuario_id"]

    hoje = datetime.today()
    
    mes = request.args.get("mes", type=int)
    ano = request.args.get("ano", type=int)

    if not mes:
        mes = hoje.month

    if not ano:
        ano = hoje.year
        
        mes = hoje.month
        ano = hoje.year
        
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

    receitas = Receita.query.filter_by(usuario_id=usuario_id).filter(
        db.extract("month", Receita.data) == mes,
        db.extract("year", Receita.data) == ano
    ).all()

    despesas = Despesa.query.filter_by(usuario_id=usuario_id).filter(
        db.extract("month", Despesa.data) == mes,
        db.extract("year", Despesa.data) == ano
    ).all()

    total_receitas = 0
    total_despesas = 0
    total_a_receber = 0
    total_a_pagar = 0
    
    qtd_receitas_pendentes = 0
    qtd_despesas_pendentes = 0

    for receita in receitas:
        if receita.recebido:
            total_receitas += receita.valor
        else:
            total_a_receber += receita.valor
            qtd_receitas_pendentes += 1

    for despesa in despesas:
        if despesa.pago:
            total_despesas += despesa.valor
        else:
            total_a_pagar += despesa.valor
            qtd_despesas_pendentes += 1

    saldo = total_receitas - total_despesas
    
    # Grafico de despesas por categoria
    despesas_por_categoria = {}
    for despesa in despesas:
        nome_categoria = despesa.categoria.nome
        cor_categoria = despesa.categoria.cor

        if nome_categoria not in despesas_por_categoria:
            despesas_por_categoria[nome_categoria] = {
                "valor": 0,
                "cor": cor_categoria
            }

        despesas_por_categoria[nome_categoria]["valor"] += despesa.valor
        
    total_grafico_despesas = 0

    for nome, dados in despesas_por_categoria.items():
        total_grafico_despesas += dados["valor"]
        
    for nome, dados in despesas_por_categoria.items():
        if total_grafico_despesas > 0:
            dados["porcentagem"] = (dados["valor"] / total_grafico_despesas) * 100
        else:
            dados["porcentagem"] = 0
            
    # Grafico de receitas por categoria
    receitas_por_categoria = {}
    for receita in receitas:
        nome_categoria = receita.categoria.nome
        cor_categoria = receita.categoria.cor

        if nome_categoria not in receitas_por_categoria:
            receitas_por_categoria[nome_categoria] = {
                "valor": 0,
                "cor": cor_categoria
            }

        receitas_por_categoria[nome_categoria]["valor"] += receita.valor


    total_grafico_receitas = 0

    for nome, dados in receitas_por_categoria.items():
        total_grafico_receitas += dados["valor"]

    for nome, dados in receitas_por_categoria.items():
        if total_grafico_receitas > 0:
            dados["porcentagem"] = (dados["valor"] / total_grafico_receitas) * 100
        else:
            dados["porcentagem"] = 0

    meta_fixada = Meta.query.filter_by(
            usuario_id=usuario_id,
            fixada=True
        ).first()

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

    return render_template(
        "index.html",
        context={
            "usuario": session.get("usuario_nome"),
            "nome_mes": meses[mes],
            "saldo": saldo,
            "total_receitas": total_receitas,
            "total_despesas": total_despesas,
            "total_a_receber": total_a_receber,
            "total_a_pagar": total_a_pagar,
            "meta_fixada": meta_fixada,
            "mes": mes,
            "ano": ano,
            "mes_anterior": mes_anterior,
            "ano_anterior": ano_anterior,
            "mes_proximo": mes_proximo,
            "ano_proximo": ano_proximo,
            "qtd_receitas_pendentes": qtd_receitas_pendentes,
            "qtd_despesas_pendentes": qtd_despesas_pendentes,
            "despesas_por_categoria": despesas_por_categoria,
            "receitas_por_categoria": receitas_por_categoria
        }
    )