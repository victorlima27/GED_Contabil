from app import app,login_manager
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuario
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash, generate_password_hash
from datetime import datetime
from flask_login import login_user, logout_user, current_user

login_manager.init_app(app)

# Configura a rota para redirecionar caso o usuário não esteja autenticado
login_manager.login_view = "login"
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.login_message_category = "danger" 

# Função para carregar o usuário no flask-login
@login_manager.user_loader
def load_user(cpf):
    return Usuario.query.get(cpf)

@app.route('/login')
def login():
    form = FormularioUsuario()
    return render_template('login.html', titulo='MEI - Login', form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)

    usuario = Usuario.query.filter_by(cpf=form.cpf.data).first()

    if usuario:
        # if usuario.ativo == True:
            senha = check_password_hash(usuario.senha_usuario, form.senha.data)
            if usuario and senha:
                login_user(usuario)
                flash(f'{usuario.nome_usuario} logado com sucesso!', 'success')
                print(f"Usuário autenticado: {current_user.email_usuario}, nome: {current_user.nome_usuario}")
                #Obtém o valor de "next" da URL, se estiver presente
                next_page = request.args.get('next')
                if next_page == None:
                    next_page = 'home'
                
                print(next_page)

                return redirect(url_for(next_page))
            else:
                flash('Senha incorreta, usuário não logado!', 'danger')
                return redirect(url_for('login'))
        # else:
        #     flash('Usuário Inativo! Favor entrar em contato com o Desenvolvimento', 'danger')
        #     return redirect(url_for('login'))
    else:
        flash('Login não existe', 'danger')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    flash('Logout efetuado com sucesso!', 'success')
    return redirect(url_for('login'))