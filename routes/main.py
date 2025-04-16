from flask import Blueprint, session, redirect, url_for, render_template, abort
from flask_login import login_required
from functools import wraps
from extensions import mysql, bcrypt, login_manager 

main_bp = Blueprint('main', __name__)

# Decorador para requerir que el usuario tenga rol "admin"
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('rol') != 'admin':
            # También podrías mostrar un template de error o redireccionar a otra página.
            return abort(403)  
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@main_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))
