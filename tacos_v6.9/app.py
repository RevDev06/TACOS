from flask import *
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required
from PIL import Image

import base64
import hashlib
import pymysql
import re
import io



from config import config
from database.db import CBD

cbd = CBD()
cbd.conectar()
conex = CBD()
conex.__init__()
user_name = "None"

csrf = CSRFProtect()
from flask import Flask

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

def comprimirImagen(image):
    img = Image.open(image)
    img = img.convert('RGB')
    img.thumbnail((1000, 1000))  
    imgComprimida = io.BytesIO()
    img.save(imgComprimida, format='JPEG', quality=90)  
    return imgComprimida.getvalue()



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
    global user_name, session, user
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
                session['logueado'] = True
                session['id'] = id_user
                return render_template("admin.html", user_name=user_name, session=session)
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
        return render_template('admin.html', user_name = user_name, session = session)
    else:
        return render_template('login.html',mensaje1 = "Esta es una vista protegida, solo para usuarios autenticados, necesitas inciar sesión como admin" )

from flask import render_template

@app.route('/products')
def products():
    cbd.cursor.execute('SELECT id, nombre, descripcion, categoria, imagen, tipo, costo, stock FROM productos')
    productos_raw = cbd.cursor.fetchall()
    
    productos = []
    for producto in productos_raw:
        productos.append({
            'id': producto[0],
            'nombre': producto[1],
            'descripcion': producto[2],
            'categoria': producto[3],
            'imagen': producto[4],
            'tipo': producto[5],
            'costo': producto[6],
            'stock': producto[7]
        })

    categorias = set([producto['tipo'] for producto in productos])

    return render_template('products.html', productos=productos, categorias=categorias)


@app.route('/guardarImg', methods=['POST'])
def saveImg():
    if request.method == 'POST':
        prdctName = request.form['nombre']
        descrip = request.form['descrip']
        categoria = request.form['categoria']
        properts = request.form['propied']
        imagen = request.files['imagen']
        tipo = imagen.mimetype
        img_comprimida = comprimirImagen(imagen)
        costo = int(request.form['costo'])
        stock = int(request.form['stock'])
        
        cbd.cursor.execute('INSERT INTO productos (nombre, descripcion, categoria, propiedades, imagen, tipo, costo, stock) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (prdctName, descrip, categoria, properts, img_comprimida, tipo, costo, stock))
        cbd.conection.commit()
    return redirect(url_for('mostrarImages'))


@app.route('/mostrarImgs')
def mostrarImages():
    cbd.cursor.execute('SELECT id, nombre, descripcion, imagen, tipo, costo, stock FROM productos')
    productos_raw = cbd.cursor.fetchall()

    productos = []
    for producto in productos_raw:
        idd, nombre, descripcion, imagen, tipo, costo, stock = producto
        imagen_base64 = base64.b64encode(imagen).decode("utf-8")
        productos.append((idd, nombre, descripcion, imagen_base64, tipo, costo, stock))

    return render_template('tablaImgs.html', products = productos, session=session, user_name = user_name)


@app.route('/addToCar', methods=['GET', 'POST'])
def addPrdctToCar():
    idUser = user[0]
    if request.method == 'POST':
        idPrdct = request.args.get('id_prdct')
        selecPrdcts = int(request.form['cantidad'])
        costo = request.args.get('precio')
    
    else:
        idPrdct = request.args.get('id_prdct')
        selecPrdcts = request.args.get('cantidad')
        costo = request.args.get('precio')
    
    try:
        cbd.cursor.execute("SELECT b.id_user, b.id_prdct, b.quant_prdcts, a.stock FROM carrito b JOIN productos a ON b.id_prdct=a.id WHERE b.id_user=%s and b.id_prdct=%s", (idUser, idPrdct))
        resul = cbd.cursor.fetchall()

        if len(resul) > 0:
            idd, idprd, cantPrds, stock = resul[0]

            if (selecPrdcts+cantPrds) > stock:
                mensaje = "Has seleccionado el límite de productos a agregar"
            
            else:
                cbd.cursor.execute("UPDATE carrito SET quant_prdcts=quant_prdcts + %s WHERE id_user=%s and id_prdct=%s", (selecPrdcts, idUser, idPrdct))
                cbd.conection.commit()

        else:
            cbd.cursor.execute("INSERT INTO carrito (id_user, id_prdct, quant_prdcts, precio_prdct) VALUES (%s, %s, %s, %s)", (idUser, idPrdct, selecPrdcts, costo))
            cbd.conection.commit()

        return redirect(url_for('verProducto', idPrdct = idPrdct))

    except pymysql.Error as err:
        return render_template('error.html', error = err)


@app.route('/updatePrdctInCar', methods=['GET', 'POST'])
def modificarPrdctInCar():
    idUser = user[0]
    if request.method == 'POST':
        idPrdct = request.args.get('id_prdct')
        #costo = request.args.get('precio')
        quantPrdcts = int(request.form['cantidad'])

    try:
        cbd.cursor.execute("UPDATE carrito SET quant_prdcts = %s WHERE id_user=%s AND id_prdct=%s", (quantPrdcts, idUser, idPrdct))
        cbd.conection.commit()

        return redirect(url_for('seePrdctSelect', idPrdctCar = idPrdct))

    except pymysql.Error as err:
        return render_template('error.html', error = err)


@app.route('/verPrdct/<string:idPrdct>')
def verProducto(idPrdct):
    idUser = user[0]

    cbd.cursor.execute("SELECT a.id, a.nombre, a.descripcion, a.categoria, a.propiedades, a.imagen, a.tipo, a.costo, a.stock, (SELECT quant_prdcts FROM carrito WHERE id_user=%s AND id_prdct=%s) AS productosCar FROM productos a WHERE a.id=%s", (idUser, idPrdct, idPrdct))
    producto_list = cbd.cursor.fetchall()

    producto = []
    for prdct in producto_list:
        idd, nombre, descrip, catego, propie, image, tipo, costo, stock, prdctsInCar = prdct
        imagen_base64 = base64.b64encode(image).decode("utf-8")
        producto.append((idd, nombre, descrip, catego, propie, imagen_base64, tipo, costo, stock, prdctsInCar))
       
    return render_template('producto.html', producto = producto)


@app.route('/verProductoSelec/<string:idPrdctCar>')
def seePrdctSelect(idPrdctCar):
    idUser = user[0]
    try:
        cbd.cursor.execute("SELECT a.id, a.nombre, a.descripcion, a.categoria, a.propiedades, a.imagen, a.tipo, a.costo, a.stock, b.quant_prdcts FROM productos a JOIN carrito b ON a.id=b.id_prdct WHERE b.id_user=%s AND a.id=%s", (idUser, idPrdctCar))
        data = cbd.cursor.fetchall()

        infoProduct = []
        for ide in data:
            idd, nombre, descripcion, catego, propert, image, tipo, costo, stock, producsSelec = ide
            total = int(producsSelec) * int(costo)
            imagen_base64 = base64.b64encode(image).decode("utf-8")
            infoProduct.append((idd, nombre, descripcion, catego, propert, imagen_base64, tipo, costo, stock, producsSelec, total))

        return render_template('productoEnCar.html', productoCar = infoProduct)

    except pymysql.Error as err:
        return render_template('error.html', error = err)


@app.route('/carrito')
def carrito():
    idUser = user[0]
    try:
        cbd.cursor.execute("SELECT id_prdct FROM carrito WHERE id_user=%s", (idUser))
        prdctsInCar = cbd.cursor.fetchall()
        
        for it in prdctsInCar:
            idd = it
            cbd.cursor.execute("SELECT a.stock, b.quant_prdcts FROM productos a JOIN carrito b ON a.id = b.id_prdct WHERE a.id = %s AND b.id_user=%s", (idd, idUser))
            productosComparar = cbd.cursor.fetchall()

            stock, userCantPrdcts = productosComparar[0]
            if (int(userCantPrdcts) > int(stock)):
                cbd.cursor.execute("UPDATE carrito SET quant_prdcts = %s WHERE id_user = %s AND id_prdct = %s", (stock, idUser, idd))


        cbd.cursor.execute("SELECT a.id, a.nombre, a.descripcion, a.imagen, a.tipo, a.costo, b.quant_prdcts FROM productos a JOIN carrito b ON a.id=b.id_prdct WHERE b.id_user=%s ORDER BY a.id", (idUser))
        data = cbd.cursor.fetchall()

        infoProducts = []
        total = 0
        for ide in data:
            idd, nombre, descripcion, image, tipo, costo, producsSelec = ide
            imagen_base64 = base64.b64encode(image).decode("utf-8")
            infoProducts.append((idd, nombre, descripcion, imagen_base64, tipo, costo, producsSelec))
            total += int(costo) * int(producsSelec)

        return render_template('carrito.html', productosCar = infoProducts, total = total)

    except pymysql.Error as err:
        return render_template('error.html', error = err)


@app.route('/eliminarPrdctCar/<string:idPrdct>')
def deletePrdctCar(idPrdct):
    idUser = user[0]
    idPrdctCar = idPrdct

    try:
        cbd.cursor.execute("DELETE FROM carrito WHERE id_user=%s and id_prdct=%s", (idUser, idPrdctCar))
        cbd.conection.commit()

        return redirect(url_for('carrito'))
    
    except pymysql.Error as err:
        return render_template('error.html', error = err)
    

@app.route('/showPrdctsAd')
def showPrdctsToAdmin():
    try:
        cbd.cursor.execute("SELECT id, nombre, descripcion, imagen, tipo, costo, stock FROM productos")
        productos = cbd.cursor.fetchall()

        infoProductos = []
        for prod in productos:
            idd, nombre, descrip, image, tipo, costo, stock = prod
            imagen_base64 = base64.b64encode(image).decode("utf-8")
            infoProductos.append((idd, nombre, descrip, imagen_base64, tipo, costo, stock))

        return render_template('readPrdcts.html', productosStore = infoProductos, session = session, user_name = user_name)
    
    except pymysql.Error as err:
        return render_template('error.html', error = err)


@app.route('/editPrdctPage/<string:idPrd>')
def updatePrdPage(idPrd):
    idPrdc = idPrd
    try:
        cbd.cursor.execute("SELECT id, nombre, descripcion, categoria, propiedades, imagen, tipo, costo, stock FROM productos WHERE id=%s", (idPrdc))
        infoPrdctToUpdt = cbd.cursor.fetchall()

        datosPrdct = []
        idd, nombre, descrip, catego, propie, image, tipo, costo, stock = infoPrdctToUpdt[0]
        imagen_base64 = base64.b64encode(image).decode("utf-8")
        datosPrdct.append((idd, nombre, descrip, catego, propie, imagen_base64, tipo, costo, stock))

        return render_template('editarPrdct.html', datosPrd = datosPrdct)
    
    except pymysql.Error as err:
        return render_template('error.html', error = err)
    

@app.route('/editPrdctInBD', methods=['GET', 'POST'])
def editPrdctBD():
    if request.method == 'POST':
        idPrd =request.args.get('idPrd')
        nombre = request.form['nombre']
        descrip = request.form['descrip']
        catego = request.form['categoria']
        properts = request.form['propied']
        imagen = request.files['imagen']
        tipo = imagen.mimetype
        img_comprimida = comprimirImagen(imagen)
        costo = int(request.form['costo'])
        stock = int(request.form['stock'])

    try:
        cbd.cursor.execute("UPDATE productos SET nombre=%s, descripcion=%s, categoria=%s, propiedades=%s, imagen=%s, tipo=%s, costo=%s, stock=%s WHERE id=%s", (nombre, descrip, catego, properts, img_comprimida, tipo, costo, stock, idPrd))
        cbd.conection.commit()

        return redirect(url_for('showPrdctsToAdmin'))

    except pymysql.Error as err:
        return render_template('error.html', error = err)
    

@app.route('/eliminPrdct/<string:idPrdct>')
def deletePrdctInBD(idPrdct):
    idPrd = idPrdct
    try:
        cbd.cursor.execute("DELETE FROM productos WHERE id=%s", (idPrd))
        cbd.conection.commit()
        cbd.cursor.execute("DELETE FROM carrito WHERE id_prdct=%s", idPrd)
        cbd.conection.commit()

        return redirect(url_for('showPrdctsToAdmin'))
    
    except pymysql.Error as err:
        return render_template('error.html', error = err)
    

@app.route('/comprar')
def comprar():
    idUser = user[0]
    try:
        cbd.cursor.execute("SELECT id_prdct, quant_prdcts, precio_prdct FROM carrito WHERE id_user=%s", (idUser))
        productosEnCar = cbd.cursor.fetchall()

        for iter in productosEnCar:
            idPrdc, cantPrdcts, precioPrd = iter
            totalPrdc = int(cantPrdcts) * int(precioPrd)

            cbd.cursor.execute("INSERT INTO compras (id_User, id_Produc, quantPrdctsBought, costoTotalPrdct) VALUES (%s, %s, %s, %s)", (idUser, idPrdc, cantPrdcts, totalPrdc))
            cbd.conection.commit()

            cbd.cursor.execute("UPDATE productos SET stock = ((SELECT stock FROM productos WHERE id=%s) - %s) WHERE id=%s", (idPrdc, cantPrdcts, idPrdc))
            cbd.conection.commit()

        cbd.cursor.execute("DELETE FROM carrito WHERE id_user=%s", (idUser))
        cbd.conection.commit()

        return redirect(url_for('mostrarImages'))

    except pymysql.Error as err:
        return render_template('error.html', error = err) 
    
@app.route('/pdp/<string:idPrdct>')
def pdp(idPrdct):
    # Aquí deberías filtrar los productos para obtener solo el que corresponde al idPrdct
    cbd.cursor.execute('SELECT id, nombre, descripcion, categoria, propiedades, imagen, tipo, costo, stock FROM productos WHERE id = %s', (idPrdct,))
    producto = cbd.cursor.fetchone()

    if producto:  # Verifica si se encontró un producto con el ID dado
        idd, nombre, descripcion, categoria,propiedades, imagen, tipo, costo, stock = producto
        imagen_base64 = base64.b64encode(imagen).decode("utf-8")
        producto = (idd, nombre, descripcion, categoria, propiedades, imagen_base64, tipo, costo, stock)
        return render_template('pdp.html', product=producto, session=session, user_name=user_name)
    else:
        # Si no se encontró el producto, puedes manejarlo como quieras, por ejemplo, mostrar un error.
        return "Producto no encontrado"
    
def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404




if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
