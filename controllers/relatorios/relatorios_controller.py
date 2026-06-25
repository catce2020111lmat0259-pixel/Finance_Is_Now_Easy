import tempfile
import matplotlib.pyplot as plt
import tempfile

from datetime import datetime
from io import BytesIO
import os

from flask import redirect, session, url_for, send_file

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER

from models.database import db
from models.receitas.receitas_model import Receita
from models.despesas.despesas_model import Despesa


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def exportar_relatorio():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    usuario_id = session["usuario_id"]
    usuario_nome = session.get("usuario_nome")

    hoje = datetime.today()

    receitas = Receita.query.filter_by(usuario_id=usuario_id).filter(
        db.extract("month", Receita.data) == hoje.month,
        db.extract("year", Receita.data) == hoje.year
    ).all()

    despesas = Despesa.query.filter_by(usuario_id=usuario_id).filter(
        db.extract("month", Despesa.data) == hoje.month,
        db.extract("year", Despesa.data) == hoje.year
    ).all()

    total_receitas = sum(r.valor for r in receitas)
    total_despesas = sum(d.valor for d in despesas)
    saldo = total_receitas - total_despesas
    
    # Análise automática
    if saldo < 0:
        titulo_analise = "Situação de atenção"
        texto_analise = (
            f"Neste período, as despesas ultrapassaram as receitas, gerando um saldo negativo de "
            f"{formatar_moeda(abs(saldo))}. \nRecomenda-se revisar os maiores gastos e priorizar despesas essenciais."
        )
    elif total_receitas > 0 and total_despesas >= total_receitas * 0.8:
        percentual = (total_despesas / total_receitas) * 100
        titulo_analise = "Situação positiva com alerta"
        texto_analise = (
            f"Embora o saldo tenha permanecido positivo, aproximadamente {percentual:.1f}% das receitas "
            f"foram\nutilizadas para cobrir despesas. Considere reduzir gastos para aumentar sua margem\nfinanceira."
        )
    else:
        titulo_analise = "Situação equilibrada"
        texto_analise = (
            f"Durante o período analisado, suas receitas foram superiores às despesas, resultando em um saldo\n positivo de "
            f"{formatar_moeda(saldo)}."
        )
        
    meses_nomes = [
        "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
        "Jul", "Ago", "Set", "Out", "Nov", "Dez"
    ]

    receitas_mes = []
    despesas_mes = []
    saldo_mes = []

    for mes in range(1, 13):
        total_receitas_mes = db.session.query(
            db.func.coalesce(db.func.sum(Receita.valor), 0)
        ).filter(
            Receita.usuario_id == usuario_id,
            db.extract("month", Receita.data) == mes,
            db.extract("year", Receita.data) == hoje.year
        ).scalar()

        total_despesas_mes = db.session.query(
            db.func.coalesce(db.func.sum(Despesa.valor), 0)
        ).filter(
            Despesa.usuario_id == usuario_id,
            db.extract("month", Despesa.data) == mes,
            db.extract("year", Despesa.data) == hoje.year
        ).scalar()

        total_receitas_mes = float(total_receitas_mes)
        total_despesas_mes = float(total_despesas_mes)
        saldo_mes_atual = total_receitas_mes - total_despesas_mes

        receitas_mes.append(total_receitas_mes)
        despesas_mes.append(total_despesas_mes)
        saldo_mes.append(saldo_mes_atual)
        
    # Cria o gráfico
    grafico_temp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    grafico_path = grafico_temp.name
    grafico_temp.close()

    plt.figure(figsize=(8, 4))

    plt.plot(meses_nomes, receitas_mes, marker="o", label="Receitas", color="#16a34a")
    plt.plot(meses_nomes, despesas_mes, marker="o", label="Despesas", color="#ef4444")
    plt.plot(meses_nomes, saldo_mes, marker="o", label="Saldo", color="#2563eb")

    plt.title("Comparativo financeiro anual")
    plt.xlabel("Meses")
    plt.ylabel("Valores em R$")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(grafico_path, dpi=160)
    plt.close()

    pdf = BytesIO()

    doc = SimpleDocTemplate(
        pdf,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    styles["Title"].alignment = TA_CENTER
    styles["Heading2"].alignment = TA_CENTER
    styles["Normal"].alignment = TA_CENTER

    elementos = []

    logo_path = os.path.join("static", "img", "fine-logo.png")

    if os.path.exists(logo_path):
        logo = Image(logo_path, width=10 * cm, height=2.5 * cm)
        logo.hAlign = "CENTER"
        elementos.append(logo)
        elementos.append(Spacer(1, 10))

    elementos.append(Paragraph("RELATÓRIO FINANCEIRO", styles["Title"]))
    elementos.append(Paragraph("Finance Is Now Easy", styles["Heading2"]))
    elementos.append(Spacer(1, 18))

    dados_identificacao = [
        ["Usuário", usuario_nome],
        ["Período", hoje.strftime("%m/%Y")],
        ["Gerado em", hoje.strftime("%d/%m/%Y %H:%M")]
    ]

    tabela_identificacao = Table(dados_identificacao, colWidths=[4 * cm, 11 * cm])
    tabela_identificacao.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef2ff")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1f2544")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    elementos.append(tabela_identificacao)
    elementos.append(Spacer(1, 22))

    elementos.append(Paragraph("Resumo financeiro", styles["Heading2"]))
    elementos.append(Spacer(1, 8))

    dados_resumo = [
        ["Receitas", "Despesas", "Saldo"],
        [formatar_moeda(total_receitas), formatar_moeda(total_despesas), formatar_moeda(saldo)]
    ]

    tabela_resumo = Table(dados_resumo, colWidths=[5 * cm, 5 * cm, 5 * cm])
    tabela_resumo.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#f8fafc")),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))
    
    elementos.append(tabela_resumo)
    elementos.append(Spacer(1, 22))

    elementos.append(Paragraph("Análise automática", styles["Heading2"]))
    elementos.append(Spacer(1, 8))

    dados_analise = [
        [titulo_analise],
        [texto_analise]
    ]

    tabela_analise = Table(dados_analise, colWidths=[15 * cm])
    tabela_analise.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef2ff")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1f2544")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    
    elementos.append(tabela_analise)
    elementos.append(Spacer(1, 22))
    
    # Grafico add ao pdf
    elementos.append(Paragraph("Comparativo financeiro anual", styles["Heading2"]))
    elementos.append(Spacer(1, 8))

    grafico_pdf = Image(grafico_path, width=15 * cm, height=7 * cm)
    grafico_pdf.hAlign = "CENTER"

    elementos.append(grafico_pdf)
    elementos.append(Spacer(1, 22))
        
    elementos.append(Paragraph("Resumo mensal do ano", styles["Heading2"]))
    elementos.append(Spacer(1, 8))

    dados_mensais = [["Mês", "Receitas", "Despesas", "Saldo"]]

    for i in range(12):
        dados_mensais.append([
            meses_nomes[i],
            formatar_moeda(receitas_mes[i]),
            formatar_moeda(despesas_mes[i]),
            formatar_moeda(saldo_mes[i])
        ])

    tabela_mensal = Table(dados_mensais, colWidths=[3 * cm, 4 * cm, 4 * cm, 4 * cm])

    tabela_mensal.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
    ]))
    
    elementos.append(tabela_mensal)
    elementos.append(Spacer(1, 22))


    elementos.append(Paragraph("Receitas", styles["Heading2"]))
    elementos.append(Spacer(1, 8))

    dados_receitas = [["Data", "Categoria", "Valor", "Status"]]

    for receita in receitas:
        dados_receitas.append([
            receita.data.strftime("%d/%m/%Y"),
            receita.categoria.nome,
            formatar_moeda(receita.valor),
            "Recebido" if receita.recebido else "Não recebido"
        ])

    if len(dados_receitas) == 1:
        dados_receitas.append(["-", "-", "Nenhuma receita cadastrada.", "-"])

    tabela_receitas = Table(dados_receitas, colWidths=[3 * cm, 4 * cm, 4 * cm, 4 * cm])
    tabela_receitas.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16a34a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elementos.append(tabela_receitas)
    elementos.append(Spacer(1, 22))

    elementos.append(Paragraph("Despesas", styles["Heading2"]))
    elementos.append(Spacer(1, 8))

    dados_despesas = [["Data", "Categoria", "Valor", "Status"]]

    for despesa in despesas:
        dados_despesas.append([
            despesa.data.strftime("%d/%m/%Y"),
            despesa.categoria.nome,
            formatar_moeda(despesa.valor),
            "Pago" if despesa.pago else "Pendente"
        ])

    if len(dados_despesas) == 1:
        dados_despesas.append(["-", "-", "Nenhuma despesa cadastrada.", "-"])

    tabela_despesas = Table(dados_despesas, colWidths=[3 * cm, 4 * cm, 4 * cm, 4 * cm])
    tabela_despesas.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#ef4444")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elementos.append(tabela_despesas)

    doc.build(elementos)
    
    try:
        os.remove(grafico_path)
    except PermissionError:
        pass

    pdf.seek(0)

    nome_arquivo = f"Relatorio_FINE_{hoje.strftime('%Y_%m')}.pdf"

    return send_file(
        pdf,
        as_attachment=True,
        download_name=nome_arquivo,
        mimetype="application/pdf"
    )