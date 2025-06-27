from flask_mail import Mail, Message

mail = Mail()

def configurar_email(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'seu_email@gmail.com'
    app.config['MAIL_PASSWORD'] = 'sua_senha_de_aplicativo'
    app.config['MAIL_DEFAULT_SENDER'] = 'seu_email@gmail.com'
    
    mail.init_app(app)

def enviar_codigo_verificacao(email_destino, codigo):
    assunto = "Seu código de verificação MFA"
    corpo = f"Olá!\n\nSeu código de verificação é: {codigo}\n\nEste código é válido por 5 minutos."
    
    msg = Message(assunto, recipients=[email_destino])
    msg.body = corpo
    mail.send(msg)
