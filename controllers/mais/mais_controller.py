from flask import render_template, redirect, url_for, session


def mais_opcoes():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    return render_template("mais/form-mais.html", context={
        "usuario": session.get("usuario_nome")
    })