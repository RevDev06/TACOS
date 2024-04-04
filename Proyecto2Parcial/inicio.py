from flask import *
import pymysql
from db import CBD
import re
import base64
from PIL import Image
import io

cbd = CBD()
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024 


def comprimirImagen(image):
    img = Image.open(image)
    img = img.convert('RGB')
    img.thumbnail((1000, 1000))  
    imgComprimida = io.BytesIO()
    img.save(imgComprimida, format='JPEG', quality=90)  
    return imgComprimida.getvalue()


@app.route('/')
def inicio():
    return render_template('iniciar.html')


@app.route('/index')
def index():
    return render_template('iniciar.html')


@app.route('/guardarImg', methods=['POST'])
def saveImg():
    if request.method == 'POST':
        prdctName = request.form['nombre']
        imagen = request.files['imagen']
        tipo = imagen.mimetype 
        imagen_comprimida = comprimirImagen(imagen)

        conection = pymysql.connect(host='localhost', user=cbd.usuarioXampp, passwd='', port=cbd.puertoXampp, db="bd_tacos")
        cursor = conection.cursor()

        cursor.execute('INSERT INTO productos (nombre, imagen, tipo) VALUES (%s, %s, %s)', (prdctName, imagen_comprimida, tipo))
        conection.commit()
    return redirect(url_for('mostrarImages'))


@app.route('/mostrarImgs')
def mostrarImages():
    conection = pymysql.connect(
        host='localhost', user=cbd.usuarioXampp, passwd='', port=cbd.puertoXampp, db="bd_tacos")
    cursor = conection.cursor()
    cursor.execute('SELECT id, nombre, imagen, tipo FROM productos')
    productos_raw = cursor.fetchall()
    productos = []
    for producto in productos_raw:
        id, nombre, imagen, tipo = producto
        imagen_base64 = base64.b64encode(imagen).decode("utf-8")
        productos.append((id, nombre, imagen_base64, tipo))

    return render_template('tablaImgs.html', products=productos)


if __name__ == "__main__":
    app.run(debug=True)
    cbd.conectar()
