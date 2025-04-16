# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from flask_login import login_required, UserMixin, login_user, logout_user
from extensions import mysql, bcrypt, login_manager  # Importa las instancias ya inicializadas
from models.user_model import UserModel

auth_bp = Blueprint('auth', __name__)
#mysql = MySQL(current_app)
#bcrypt = Bcrypt(current_app)

# Aquí definimos la clase de usuario para Flask-Login
class User(UserMixin):
    pass

# Configuramos el 'user_loader' de Flask-Login
@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, password_hash, rol FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        user = User()
        user.id = user_data[0]
        user.username = user_data[1]
        user.email = user_data[2]
        user.password_hash = user_data[3]
        user.rol = user_data[4]
        return user
    return None

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, email, password_hash, rol FROM users WHERE username = %s", (username,))
        user_data = cur.fetchone()
        cur.close()
        
        if user_data and bcrypt.check_password_hash(user_data[3], password):
            user = User()
            user.id = user_data[0]
            session['rol'] = user_data[4]
            session['username'] = user_data[1]
          
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            error = "Usuario o contraseña incorrectos. Por favor, verifica tus datos e inténtalo nuevamente."
    
    return render_template('login.html', error=error)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if 'rol' in session and session['rol'] == 'admin':
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            rol = request.form['rol']
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, email, password_hash, rol) VALUES (%s, %s, %s, %s)", 
                        (username, email, hashed_password, rol))
            mysql.connection.commit()
            cur.close()
            return jsonify({'success': True, 'message': '¡Usuario agregado satisfactoriamente!'})
        
        return render_template('create_user.html')
    else:
        return jsonify({'success': False, 'message': 'No tienes permisos para realizar esta acción.'}), 403

@auth_bp.route('/list_users')
@login_required
def list_users():
    if 'rol' in session and session['rol'] == 'admin':
        user_model = UserModel(mysql)
        users = user_model.get_all_users()
        return render_template('list_users.html', users=users)
    else:
        return "Acceso no autorizado", 403

# Función para la creación inicial del superusuario
#@auth_bp.before_app_first_request
def create_admin_user():
    cur = mysql.connection.cursor()
    hashed_password = bcrypt.generate_password_hash('15111974').decode('utf-8')
    try:
        cur.execute("SELECT id FROM users WHERE username = 'admin'")
        if cur.fetchone() is None:
            cur.execute("INSERT INTO users (username, email, password_hash, rol) VALUES (%s, %s, %s, %s)", 
                        ('admin', 'admin@ucim.com', hashed_password, 'admin'))
            mysql.connection.commit()
            current_app.logger.info("Superusuario creado con éxito")
        else:
            current_app.logger.info("El superusuario ya existe")
    except Exception as e:
        current_app.logger.error(f"Error al crear el superusuario: {e}")
    finally:
        cur.close()
