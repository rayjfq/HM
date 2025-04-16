# extensions.py

from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

mysql = MySQL()       # No se pasa app acá
bcrypt = Bcrypt()     # No se pasa app acá
login_manager = LoginManager()  # No se pasa app acá
