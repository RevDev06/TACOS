from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required,UserMixin
from config import config
import pymysql

from models.entities.register import Register

from models.ModelUser import ModelUser
from models.entities.user import User

from models.db import CBD

cbd = CBD()
cbd.conectar()
app = Flask(__name__)

csrf = CSRFProtect()
login_manager_app = LoginManager(app)




@app.route('/')
def home():
    return render_template('home.html')


# R E G I S T R O
@app.route('/registro')
def registro():
    return render_template('registro.html')  

@app.route('/crear-registro', methods= ["GET", "POST"])
def crear_registro(): 
    
    nombrec=request.form['nombrec'] 
    correo=request.form['correo']
    numcel=request.form['numcel']
    direc=request.form['direc']
    contraseña=request.form['contraseña_encriptada']
    
    cbd.cursor.execute(" INSERT INTO usuarios (nombrec, correo, numcel, direc, contraseña, id) VALUES (%s, %s, %s, %s, %s, '4')",(nombrec,correo,numcel,direc,contraseña))
    cbd.conection.commit()

    cbd.cursor.close()
    cbd.conection.close()    

    return render_template("register.html",mensaje="Usuario Registrado Exitosamente")

# T E R M I N O

# I N I C I O  D E  S E S I Ó N

class User(UserMixin):
    def __init__(self, id, correo, contraseña):
        self.id = id
        self.correo = correo
        self.contraseña = contraseña

@login_manager_app.user_loader
def load_user(id):
    sql = "SELECT id, correo, contraseña FROM usuarios WHERE id = %s"
    with cbd.conection.cursor() as cursor:
        cursor.execute(sql, (id,))
        user_data = cursor.fetchone()
        if user_data:
            # Si se encuentra el usuario en la base de datos, crea un objeto User y devuélvelo
            user = User(user_data[0], user_data[1], user_data[2])
            return user
        else:
            # Si no se encuentra el usuario, devuelve None
            return None

@app.route('/acceso-login', methods= ["GET", "POST"])
def login():
   
    if request.method == 'POST' and 'correo' in request.form and 'contraseña' in request.form:
       
        _correo = request.form['correo']
        _password = request.form['contraseña']

        cur = cbd.conection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s', (_correo, _password,))
        account = cur.fetchone()
      
        if account:
            session['logueado'] = True
            session['id'] = account['id']

            return render_template("admin.html")
        else:
            return render_template('index.html',mensaje="Usuario O Contraseña Incorrectas")

# T E R M I N O

# C E R R A R  S E S I Ó N

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# T E R M I N O

@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()