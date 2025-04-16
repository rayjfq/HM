from flask import Blueprint, render_template, request, session, jsonify
from flask_login import login_required
from models.patient_model import PatientModel
#from app import mysql  # Asegúrate de que mysql esté declarado en tu app principal
from extensions import mysql, bcrypt, login_manager 

patients_bp = Blueprint('patients', __name__, url_prefix='/patients')

@patients_bp.route('/list')
@login_required
def list_patients():
    patient_model = PatientModel(mysql)
    patients = patient_model.get_all_patients()
    return render_template('list_patients.html', patients=patients)

@patients_bp.route('/add', methods=['POST'])
@login_required
def add_patient():
    if 'rol' in session and session['rol'] == 'admin':
        patient_id    = request.form['patient_id']
        name          = request.form['name']
        last_name     = request.form['last_name']
        age           = request.form['age']
        gender        = request.form['gender']
        birth_date    = request.form['birth_date']
        patient_record= request.form['patient_record']
        diagnosis     = request.form['diagnosis']

        patient_model = PatientModel(mysql)
        # Validación: comprueba si el patient_id ya existe
        existing_patient = patient_model.get_patient_by_id(patient_id)
        if existing_patient:
            return jsonify({
                'success': False,
                'message': 'El documento de identidad ya existe. Por favor verifique o ingrese otro.'
            }), 400

        # Si no existe, se procede a agregarlo
        patient_model.add_patient(patient_id, name, last_name, age, gender, birth_date, patient_record, diagnosis)
        return jsonify({'success': True, 'message': '¡Paciente agregado satisfactoriamente!'})
    else:
        return jsonify({'success': False, 'message': 'No tienes permisos para realizar esta acción.'}), 403
