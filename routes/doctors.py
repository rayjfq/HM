from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required
from models.doctor_model import DoctorModel
#from app import mysql
from extensions import mysql, bcrypt, login_manager 

doctors_bp = Blueprint('doctors', __name__, url_prefix='/doctors')

@doctors_bp.route('/list')
@login_required
def list_doctors():
    doctor_model = DoctorModel(mysql)
    doctors = doctor_model.get_all_doctors()
    return render_template('list_doctors.html', doctors=doctors)

@doctors_bp.route('/add', methods=['POST'])
@login_required
def add_doctor():
    if 'rol' in session and session['rol'] == 'admin':
        doctor_id = request.form['doctor_id']
        name      = request.form['name']
        last_name = request.form['last_name']
        title     = request.form['title']
        email     = request.form['email']
        specialty = request.form['specialty']

        doctor_model = DoctorModel(mysql)
        # Validación: comprueba si el doctor_id ya existe
        existing_doctor = doctor_model.get_doctor_by_id(doctor_id)
        if existing_doctor:
            return jsonify({
                'success': False,
                'message': 'El documento de identidad ya existe. Por favor verifique o ingrese otro.'
            }), 400

        # Si no existe, se procede a agregarlo
        doctor_model.add_doctor(doctor_id, name, last_name, title, email, specialty)
        return jsonify({'success': True, 'message': '¡Doctor agregado satisfactoriamente!'})
    else:
        return jsonify({'success': False, 'message': 'No tienes permisos para realizar esta acción.'}), 403
