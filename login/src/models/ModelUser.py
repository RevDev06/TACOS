from .entities.user import User


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, correo, contraseña, nombrec FROM usuario 
                    WHERE nombrec = '{}'""".format(user.correo)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = user(row[0], row[1], user.check_password(row[2], user.contraseña), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, correo, nombrec FROM usuario WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)