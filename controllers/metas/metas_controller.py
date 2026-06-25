from flask import render_template, request, redirect, url_for, session
from models.metas.metas_model import Meta
from models.database import db


def criar_meta():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    return render_template("metas/form-criar-meta.html")


def salvar_meta():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        conteudo = request.form.get("conteudo")

        meta = Meta(
            conteudo=conteudo,
            usuario_id=session["usuario_id"]
        )

        errors = meta.validate()

        context = {
            "meta": meta
        }

        if not errors:
            db.session.add(meta)
            db.session.commit()

            context["sucesso"] = "Meta criada com sucesso!"
            return redirect(url_for("listar_metas"))
        else:
            context["erros"] = errors
            return render_template("metas/form-criar-meta.html", context=context)


    return redirect(url_for("criar_meta"))


def listar_metas():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    pesquisa = request.args.get("pesquisa", "").strip()

    query = Meta.query.filter_by(usuario_id=session["usuario_id"])

    if pesquisa:
        query = query.filter(Meta.conteudo.ilike(f"%{pesquisa}%"))

    metas = query.all()
    
    context = {
        "metas": metas,
        "pesquisa": pesquisa
    }

    return render_template("metas/form-listar-meta.html", context=context)


def editar_meta(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    meta = Meta.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()

    if not meta:
        return redirect(url_for("listar_metas"))

    if request.method == "POST":
        meta.conteudo = request.form.get("conteudo")

        errors = meta.validate()

        if not errors:
            db.session.commit()
            return redirect(url_for("listar_metas"))

        context = {
            "meta": meta,
            "erros": errors
        }

        return render_template("metas/form-editar-meta.html", context=context)

    return render_template("metas/form-editar-meta.html", context={"meta": meta})


def confirmar_exclusao_meta(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    meta = Meta.query.filter_by(id=id, usuario_id=session["usuario_id"]).first()

    if not meta:
        return redirect(url_for("listar_metas"))

    if request.method == "POST":
        confirmacao = request.form.get("confirmar-exclusao")

        if confirmacao == "Sim":
            db.session.delete(meta)
            db.session.commit()

    return redirect(url_for("listar_metas"))

def fixar_meta(id):
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    metas = Meta.query.filter_by(usuario_id=session["usuario_id"]).all()

    for meta in metas:
        meta.fixada = False

    meta_escolhida = Meta.query.filter_by(
        id=id,
        usuario_id=session["usuario_id"]
    ).first()

    if meta_escolhida:
        meta_escolhida.fixada = True
        db.session.commit()

    return redirect(url_for("listar_metas"))