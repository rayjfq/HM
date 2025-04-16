from flask_mysqldb import MySQL

class UserModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_all_users(self):
        """Obtiene todos los usuarios de la base de datos."""
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT id, username, email, rol FROM users")
        users = cur.fetchall()
        cur.close()
        return users
