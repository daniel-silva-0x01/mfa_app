from flask import Flask, render_template, request, redirect, url_for, session
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'segredo123'

USUARIO = {'usuario': 'senha123'}

EXPIRACAO_CODIGO_MINUTOS = 5

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['usuario']
        senha = request.form['senha']
        if user in USUARIO and USUARIO[user] == senha:
            codigo = str(random.randint(100000, 999999))
            session['codigo_verificacao'] = codigo
            session['usuario'] = user
            
            session['codigo_gerado_em'] = datetime.now().isoformat()
            return redirect(url_for('verificar'))
        else:
            return "Usuário ou senha inválidos"
    return render_template('login.html')

@app.route('/verificar', methods=['GET', 'POST'])
def verificar():
    codigo_gerado_em_str = session.get('codigo_gerado_em')
    if not codigo_gerado_em_str:
        return redirect(url_for('login'))  

    codigo_gerado_em = datetime.fromisoformat(codigo_gerado_em_str)
    tempo_agora = datetime.now()

    
    if tempo_agora > codigo_gerado_em + timedelta(minutes=EXPIRACAO_CODIGO_MINUTOS):
        
        session.pop('codigo_verificacao', None)
        session.pop('codigo_gerado_em', None)
        return "Código expirado! Por favor, faça login novamente."

    if request.method == 'POST':
        codigo = request.form['codigo']
        if codigo == session.get('codigo_verificacao'):
            return redirect(url_for('sucesso'))
        else:
            return "Código incorreto!"
    return render_template('verify.html', codigo=session['codigo_verificacao'])

@app.route('/sucesso')
def sucesso():
    return render_template('success.html', usuario=session.get('usuario'))

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('certificado.pem', 'chave.pem'))

