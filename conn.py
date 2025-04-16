from flask_mysqldb import MySQL
from flask import Flask

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '15111974'
app.config['MYSQL_DB'] = 'historia_medica'

mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute('SELECT 1')
    print('Conexión exitosa')
