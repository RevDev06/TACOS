import re

def getXamppPort(rutaXampp='C:/xampp/mysql/bin/my.ini'):
    try:
        with open(rutaXampp, 'r') as archivo:
            contenido = archivo.read()


        resultado = re.search(r'port[ ]*=[ ]*(\d+)', contenido)
        if resultado:
            return int(resultado.group(1))  
        else:
            print("No hay puerto predeterminado")
            return None
    except FileNotFoundError:
        print(f"No se encontro Xampp en la ruta {rutaXampp}")
        return None

def getApachePort(rutaApache='C:/xampp/apache/conf/httpd.conf'):
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
        return None

puertoXampp = getXamppPort()
puertoApache = getApachePort()
if puertoXampp:
    print(f"El puerto de mysql es {puertoXampp}")
else:
    print("No se pudo encontrar")

if puertoApache:
    print(f"El puerto de apache es {puertoApache}")
else:
    print("No se pudo encontrar")