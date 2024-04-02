import re
import mysql.connector
from mysql.connector import Error as ex
import pymysql
from pymysql import Error as err

class CBD():
    def detectarPuerto(rutaXampp='C:/xampp/mysql/bin/my.ini'):
        try:
            with open(rutaXampp, 'r') as archivo:
                contenido = archivo.read()


            resultado_puerto = re.search(r'port[ ]*=[ ]*(\d+)', contenido)
            if resultado_puerto:
                puerto = int(resultado_puerto.group(1))  

            else:
                print("No hay puerto predeterminado")
                puerto =  None
            
            resultado_usuario = re.search(r'user[ ]*=[ ]*(\w+)', contenido)
            if resultado_usuario:
                usuario = resultado_usuario.group(1)
            else:
                print("No se encontró un nombre de usuario")
                usuario = None

            return puerto, usuario

        except FileNotFoundError:
            print(f"No se encontro Xampp en la ruta {rutaXampp}")
            return None, None

    # Uso de la función
    puerto, usuario = detectarPuerto()
    if puerto:
        print(f"\nEl puerto de MySQL es {puerto}")
        print(f"El nombre de usuario de MySQL es {usuario}")
    else:
        print("No se pudo encontrar")


    def crearDB():
        try:
            conection = pymysql.connect(host='localhost', user='root', passwd='', port=puerto)
            cursor = conection.cursor()
            cursor.execute("CREATE DATABASE proyecto")
            conection.close()
            print("\nCreacion exitosa")
        except ex and err: 
            print ("\nError al intentar la creación: {0}".format(ex))
            print ("\nError al intentar la creación: @ {0}".format(err))

    def crearTablaUsuar():
        try:
            conection = pymysql.connect(host='localhost', user='root', passwd='', port=puerto, db="proyecto")
            cursor = conection.cursor()
            cursor.execute("CREATE TABLE usuario (id int AUTO_INCREMENT PRIMARY KEY, nombre varchar(50), apellidos varchar(50), correo varchar(60), direccion varchar(100), contraseña varchar(20), contraseña2 varchar(20))")
            conection.close()
        except ex and err:
            print("\nError al crear la tabla Usuario: {0}".format(err))

    def crearTablaCate():
        try:
            conection = pymysql.connect(host='localhost', user='root', passwd='', port=puerto, db="proyecto")
            cursor = conection.cursor()
            cursor.execute("CREATE TABLE categoria (id int AUTO_INCREMENT PRIMARY KEY, nombre varchar(50))")
            conection.close()
        except ex and err:
            print("\nError al crear la tabla Categoría: {0}".format(err))

    def crearTablaProducts():
        try:
            conection = pymysql.connect(host='localhost', user='root', passwd='', port=puerto, db="proyecto")
            cursor = conection.cursor()
            cursor.execute("CREATE TABLE productos (id int AUTO_INCREMENT PRIMARY KEY, nombre varchar(50), descripcion varchar(300), propiedades varchar(300), costo int, stock int, id_cate int)")
            conection.close()
        except ex and err:
            print("\nError al crear la tabla Productos: {0}".format(err))

    def conectar():
        try:
            crearDB()
            crearTablaUsuar()
            crearTablaCate()
            crearTablaProducts()
        except ex and err: 
            print ("\nError al intentar la conexión: {0}".format(ex))
            print ("\nError al intentar la conexión: @ {0}".format(err))


cbd = CBD()
cbd.conectar()

# categoria id, nombre
# productos id, nombre, costo, stock, descripcion, imagen, propiedades, id_cate