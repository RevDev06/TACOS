import re

def detectarPuerto(rutaXampp='C:/xampp/mysql/bin/my.ini'):
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

# Uso de la función
puerto = detectarPuerto()
if puerto_mysql:
    print(f"El puerto de mysql es {puerto}")
else:
    print("No se pudo encontrar")
