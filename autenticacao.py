from flask import request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from database import conectar
import jwt
import datetime

SECRET_KEY = "sua_chave_super_secreta"

def registrar_usuario():
    data = request.get_json()
    username = data.get("nomeusuario")
    email = data.get("email")
    senha = data.get("senha")

    if not username or not senha or not email:
        return jsonify({"erro": "Dados incompletos."}), 400

    senha_hash = generate_password_hash(senha)
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO usuarios (nomeusuario, email, senha) VALUES (?, ?, ?)",
                    (nomeusuario, email, senha))
        con.commit()
        return jsonify({"mensagem": "Usuário registrado com sucesso!"})
    except:
        return jsonify({"erro": "Usuário ou e-mail já existem."}), 400
    finally:
        con.close()

def registrar_usuario_com_formulario(request):
    nomeusuario = request.form.get("nomeusuario")
    email = request.form.get("email")
    senha = request.form.get("senha")

    if not nomeusuario or not email or not senha:
        return "Preencha todos os campos", 400

    senha_hash = generate_password_hash(senha)
    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO usuarios (nomeusuario, email, senha) VALUES (?, ?, ?)",
                    (nomeusuario, email, senha_hash))
        con.commit()
        return redirect(url_for("verificar_codigo_mfa"))
    except:
        return "Usuário ou e-mail já existem", 400
    finally:
        con.close()

def fazer_login():
    data = request.get_json()
    username = data.get("username")
    senha = data.get("password")

    if not username or not senha:
        return jsonify({"erro": "Usuário e senha são obrigatórios."}), 400

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT id, senha FROM usuarios WHERE nomeusuario = ?", (nomeusuario,))
    user = cur.fetchone()
    con.close()

    if user and check_password_hash(user[1], senha):
        token = jwt.encode(
            {
                "user_id": user[0],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"token": token})
    else:
        return jsonify({"erro": "Credenciais inválidas."}), 401
