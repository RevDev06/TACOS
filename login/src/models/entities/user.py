from werkzeug.security import check_password_hash
from register import Register

class User():

    def __init__(self, id, correo, contraseña_encriptada ) -> None:
        self.id = id
        self.correo = correo
        self.contraseña = contraseña_encriptada

    @classmethod
    def check_password(self,hashed_contraseña,contraseña):
        return check_password_hash(hashed_contraseña, contraseña)
