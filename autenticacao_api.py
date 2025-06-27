from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import conectar
import jwt
import datetime

CHAVE_SECRETA = "sua_chave_super_secreta"

def registrar_usuario_api():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    senha = data.get("password")

    if not username or not email or not senha:
        return jsonify({"erro": "Preencha todos os campos."}), 400

    senha_hash = generate_password_hash(senha)

    con = conectar()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO usuarios (nomeusuario, email, senha) VALUES (?, ?, ?)",
                    (username, email, senha_hash))
        con.commit()
        return jsonify({"mensagem": "Usuário registrado com sucesso!"})
    except:
        return jsonify({"erro": "Usuário ou e-mail já existem."}), 400
    finally:
        con.close()

def fazer_login_api():
    data = request.get_json()
    username = data.get("username")
    senha = data.get("password")

    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, senha FROM usuarios WHERE nomeusuario = ?", (username,))
    user = cur.fetchone()
    con.close()

    if user and check_password_hash(user[1], senha):
        token = jwt.encode(
            {"user_id": user[0], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)},
            CHAVE_SECRETA,
            algorithm="HS256"
        )
        return jsonify({"token": token})
    else:
        return jsonify({"erro": "Usuário ou senha inválidos."}), 401
