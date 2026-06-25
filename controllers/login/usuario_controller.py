from sqlalchemy.exc import IntegrityError

from flask import render_template, request, redirect, url_for, session
from models.login.usuario_model import Usuario
from models.database import db

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash


def login():
    if "usuario_id" in session:
        return redirect(url_for("home"))

    return render_template("login/form-login.html")

def esqueci_senha():
    return render_template("login/form-esqueci-senha.html")

def criar_usuario():
    return render_template("login/form-criar-usuario.html")

def salvar_usuario():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    data_nascimento = request.form.get("data_nascimento")
    pergunta_secreta = request.form.get("pergunta_secreta")
    resposta_secreta = request.form.get("resposta_secreta")

    errors = []

    if not data_nascimento:
        errors.append("Data de nascimento é obrigatória.")
        return render_template("login/form-criar-usuario.html", context={"erros": errors})

    data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()

    usuario_existente = Usuario.query.filter_by(email=email).first()

    if usuario_existente:
        errors.append("Já existe um usuário com esse email.")
        return render_template("login/form-criar-usuario.html", context={"erros": errors})

    usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha,
        data_nascimento=data_nascimento,
        pergunta_secreta=pergunta_secreta,
        resposta_secreta=resposta_secreta
    )

    errors = usuario.validate()

    if not errors:
        try:
            usuario.senha = generate_password_hash(senha)
            
            db.session.add(usuario)
            db.session.commit()

            return render_template("login/form-criar-usuario.html", context={
                "usuario": usuario,
                "sucesso": "Usuário cadastrado com sucesso!"
            })

        except IntegrityError:
            db.session.rollback()

            return render_template("login/form-criar-usuario.html", context={
                "usuario": usuario,
                "erros": ["Já existe um usuário com esse email."]
            })

    return render_template("login/form-criar-usuario.html", context={
        "usuario": usuario,
        "erros": errors
    })
    
def autenticar():
    email = request.form.get("email")
    senha = request.form.get("senha")

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and check_password_hash(usuario.senha, senha):
        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome

        return redirect(url_for("home"))

    return render_template(
        "login/form-login.html",
        context={
            "erros": ["Email ou senha inválidos."]
        }
    )
    
def logout():
    session.clear()
    return redirect(url_for("login"))

def usuario_logado():
    return "usuario_id" in session

def verificar_recuperacao():
    email = request.form.get("email")
    data_nascimento = request.form.get("data_nascimento")
    pergunta_secreta = request.form.get("pergunta_secreta")
    resposta_secreta = request.form.get("resposta_secreta")

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return render_template(
            "login/form-esqueci-senha.html",
            context={
                "erros": ["Dados inválidos."]
            }
        )

    data_nascimento = datetime.strptime(
        data_nascimento,
        "%Y-%m-%d"
    ).date()

    if (
        usuario.data_nascimento == data_nascimento
        and usuario.pergunta_secreta == pergunta_secreta
        and usuario.resposta_secreta.lower() == resposta_secreta.lower()
    ):
        return render_template(
            "login/form-nova-senha.html",
            context={
                "usuario_id": usuario.id
            }
        )

    return render_template(
        "login/form-esqueci-senha.html",
        context={
            "erros": ["Dados inválidos."]
        }
    )
    
def salvar_nova_senha():
    usuario_id = request.form.get("usuario_id")
    senha = request.form.get("senha")
    confirmar_senha = request.form.get("confirmar_senha")

    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return redirect(url_for("login"))

    errors = []

    if senha != confirmar_senha:
        errors.append("As senhas devem ser iguais.")
        
    usuario.senha = senha
    errors += usuario.validate_senha()

    if errors:
        return render_template(
            "login/form-nova-senha.html",
            context={
                "usuario_id": usuario.id,
                "erros": errors
            }
        )

    usuario.senha = generate_password_hash(senha)

    db.session.commit()

    return render_template(
        "login/form-login.html",
        context={
            "sucesso": "Senha alterada com sucesso! Faça login novamente."
        }
    )