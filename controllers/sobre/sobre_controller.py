from flask import render_template, redirect, url_for, session

def sobre():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    return render_template("sobre/sobre.html")