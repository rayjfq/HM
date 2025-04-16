# app.py
from flask import Flask
from config import Config
from extensions import mysql, bcrypt, login_manager
from routes import register_blueprints

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa las extensiones con la aplicación
mysql.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

register_blueprints(app)

# Ejemplo con before_request para inicialización única (si lo necesitas)
admin_initialized = False
@app.before_request
def init_admin_once():
    global admin_initialized
    if not admin_initialized:
        from routes.auth import create_admin_user  # Asegúrate de importarlo aquí
        create_admin_user()
        admin_initialized = True

if __name__ == '__main__':
    app.run(debug=True)




