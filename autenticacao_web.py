from flask import request, redirect, url_for, session
from werkzeug.security import generate_password_hash
from database import conectar

def registrar_usuario_formulario():
    nomeusuario = request.form.get("nomeusuario")
    email = request.form.get("email")
    senha = request.form.get("senha")

    if not nomeusuario or not email or not senha:
        return "Preencha todos os campos.", 400

    senha_hash = generate_password_hash(senha)

    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO usuarios (nomeusuario, email, senha) VALUES (?, ?, ?)",
                    (nomeusuario, email, senha_hash))
        con.commit()

        session['usuario'] = nomeusuario
        session['email'] = email
        return redirect(url_for("verificar_codigo_mfa"))

    except:
        return "Usuário ou e-mail já existem.", 400
    finally:
        con.close()
