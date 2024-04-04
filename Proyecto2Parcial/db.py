import re
#import mysql.connector
#from mysql.connector import Error as ex
import pymysql

class CBD():

    def detectarPuertosXampp(rutaXampp='C:/xampp/mysql/bin/my.ini'):
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
                usuario = "root"

            return puerto, usuario

        except FileNotFoundError:
            print(f"No se encontro Xampp en la ruta {rutaXampp}")
            return None, None
        

    """def detectarPuertoApache(rutaApache='C:/xampp/apache/conf/httpd.conf'):
        try:
            with open(rutaApache, 'r') as archivo:
                contenido = archivo.read()


            resultados = re.findall(r'^Listen[ ]+(\d+)', contenido, re.MULTILINE)
            if resultados:
                return [int(puerto) for puerto in resultados]
            else:
                print("No se encontraron datos 'Listen' en el archivo")
                return None
        except FileNotFoundError:
            print(f"No se pudo encontrar el archivo de configuración en {rutaApache}.")
            return None"""


    puertoXampp, usuarioXampp = detectarPuertosXampp()
    if puertoXampp:
        print(f"\nEl puerto de MySQL es {puertoXampp}")
        print(f"El nombre de usuario de MySQL es {usuarioXampp}")
    else:
        print("No se pudo encontrar el puerto de Xampp")


    """puertoApache = detectarPuertoApache()
    if puertoApache:
        print(f"El puerto de Apache es {puertoApache}")
    else:
        print("No se pudo encontrar")"""



    def crearDB(self):
        try:
            conection = pymysql.connect(host='localhost', user=self.usuarioXampp, passwd='', port=self.puertoXampp)
            cursor = conection.cursor()
            cursor.execute("CREATE DATABASE if not exists bd_tacos")
            conection.close()
            print("\nCreacion exitosa")
        except pymysql.Error as err: 
            print ("\nError al intentar la creación de la BD: {0}".format(err))


    def crearTablaUsuar(self):
        try:
            conection = pymysql.connect(host='localhost', user=self.usuarioXampp, passwd='', port=self.puertoXampp, db="bd_tacos")
            cursor = conection.cursor()
            cursor.execute("CREATE TABLE if not exists usuario (id int AUTO_INCREMENT PRIMARY KEY, nombre varchar(50), apellidos varchar(50), correo varchar(60), direccion varchar(100), contraseña varchar(20), contraseña2 varchar(20))")
            conection.close()
        except pymysql.Error as err:
            print("\nError al crear la tabla Usuario: {0}".format(err))


    def crearTablaCate(self):
        try:
            conection = pymysql.connect(host='localhost', user=self.usuarioXampp, passwd='', port=self.puertoXampp, db="bd_tacos")
            cursor = conection.cursor()
            cursor.execute("CREATE TABLE if not exists categoria (id int AUTO_INCREMENT PRIMARY KEY, nombre varchar(50))")
            conection.close()
        except pymysql.Error as err:
            print("\nError al crear la tabla Categoría: {0}".format(err))


    def crearTablaProducts(self):
        try:
            conection = pymysql.connect(host='localhost', user=self.usuarioXampp, passwd='', port=self.puertoXampp, db="bd_tacos")
            cursor = conection.cursor()
            cursor.execute("CREATE TABLE if not exists productos (id int AUTO_INCREMENT PRIMARY KEY, nombre varchar(50), descripcion varchar(300), propiedades varchar(300), imagen longblob, tipo varchar(50), costo int, stock int, id_cate int)")
            conection.close()
        except pymysql.Error as err:
            print("\nError al crear la tabla Productos: {0}".format(err))


    def conectar(self):
        try:
            self.crearDB()
            self.crearTablaUsuar()
            self.crearTablaCate()
            self.crearTablaProducts()
        except pymysql.Error as err: 
            print ("\nError al intentar la conexión:  {0}".format(err))


cbd = CBD()
cbd.conectar()

# categoria id, nombre
# productos id, nombre, costo, stock, descripcion, imagen, propiedades, id_cate