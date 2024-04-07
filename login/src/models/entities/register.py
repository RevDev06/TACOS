from werkzeug.security import generate_password_hash, check_password_hash

class Register():

    def __init__(self, id, nombrec, correo, numcel, direc, contraseña, contraseña1) -> None:
        self.id = id
        self.nombrec = nombrec
        self.correo = correo
        self.numcel = numcel
        self.direc = direc
        self.contraseña = contraseña
        self.contraseña1 = contraseña1

        if contraseña == contraseña1:
            self.contraseña_encriptada = generate_password_hash(contraseña1, 'sha256', 30)
