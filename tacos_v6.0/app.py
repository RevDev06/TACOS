from flask import *
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required

import hashlib
import pymysql
import re

from config import config
from database.db import CBD

cbd = CBD()
cbd.conectar()
conex = CBD()
conex.__init__()


csrf = CSRFProtect()
from flask import Flask

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')


app = Flask(__name__)




@app.route('/')
def home():
    return render_template("home.html", user_name=user_name, session=session)

# R E G I S T R O

@app.route('/registro')
def registro():
    return render_template('registro.html')  

@app.route('/crear_registro', methods=["GET","POST"])
def crear_registro(): 
    if request.method in ["GET","POST"]:
        nombrec = request.form['nombrec'] 
        correo = request.form['correo']
        numcel = request.form['numcel']
        direccion = request.form['direccion']
        contraseña = request.form['contraseña']
        contraseña1 = request.form['contraseña1']

        try:
            cbd.cursor.execute("SELECT correo FROM usuario WHERE correo = %s", (correo,))
            us_existente = cbd.cursor.fetchone()

            if us_existente:
                return render_template("registro.html", mensaje="Con este correo ya existe una cuenta")

            if contraseña == contraseña1:

                contraseña_encriptada = generate_password_hash(contraseña1)
                
                cbd.cursor.execute("INSERT INTO usuario (nombrec, correo, numcel, direccion, contraseña_encriptada) VALUES (%s, %s, %s, %s, %s)",(nombrec,correo,numcel,direccion,contraseña_encriptada))
                cbd.conection.commit()
                
                return render_template("registro.html", mensaje="Usuario creado exitosamente")
            else:
                return render_template("registro.html", mensaje="Las contraseñas no coinciden")
            
        except Exception as e:
            cbd.conection.rollback()
            return f"Error: {str(e)}"    

    else:
        return render_template("registro.html", mensaje="Método no permitido")


# T E R M I N O

# I N I C I O  D E  S E S I Ó N
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

from flask import request, render_template

@app.route('/entrar_login', methods=['GET', 'POST'])
def entrar_login():
    global user_name, session
    if request.method == 'POST' and 'correo' in request.form and 'contraseña':
        _correo = request.form['correo']
        _contraseña = request.form['contraseña']

        cur = cbd.cursor
        cur.execute('SELECT id, nombrec, correo, contraseña_encriptada FROM usuario WHERE correo = %s', (_correo,))
        user = cur.fetchone()

        if user:
            id_user = user[0]
            user_name = user[1].split()[:2]  # Dividir el nombre en las primeras dos palabras
            correo_bd = user[2]
            contraseña_encriptada_bd = user[3]

            if _correo == "admin@gmail.com" and _contraseña == 'B!1w8NAt1T^%kvhUI*S^':
                return render_template("admin.html")
            else:
                if check_password_hash(contraseña_encriptada_bd, _contraseña):
                    session['logueado'] = True
                    session['id'] = id_user

                    return render_template("home.html", user_name=user_name, session=session)
                else:
                    return render_template("login.html", mensaje1="La contraseña no coincide")
        else:
            return render_template("login.html", mensaje1="Por favor, ingrese su correo y contraseña")
    return render_template("login.html", mensaje1="Por favor, ingrese su correo y contraseña")

# T E R M I N O

# C I E R R E  D E  S E S I Ó N

@app.route('/logout')
def logout():

    session.pop('username', None)
    session.pop('logueado', None)
    session.pop('id', None)
    return render_template('login.html')


# T E R M I N O


@app.route('/admin')
def admin():
    if 'admin' in session and session['admin']:
        return render_template('admin.html')
    else:
        return render_template('login.html',mensaje1 = "Esta es una vista protegida, solo para usuarios autenticados, necesitas inciar sesión como admin" )

@app.route('/products')
def products():
    return render_template("products.html", user_name=user_name, session=session)

def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()