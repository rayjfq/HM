from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required
from models.medical_history_model import MedicalHistoryModel
#from app import mysql
from extensions import mysql, bcrypt, login_manager 

histories_bp = Blueprint('histories', __name__, url_prefix='/histories')

@histories_bp.route('/list')
@login_required
def list_history():
    medical_history_model = MedicalHistoryModel(mysql)
    histories = medical_history_model.get_all_histories()
    return render_template('list_history.html', histories=histories)

@histories_bp.route('/add', methods=['POST'])
@login_required
def add_history():
    if 'rol' in session and session['rol'] == 'admin':
        history_id      = request.form['history_id']
        patient_id      = request.form['patient_id']
        doctor_id       = request.form['doctor_id']
        diagnosis       = request.form['diagnosis']
        observation     = request.form['observation']
        observation_date= request.form['observation_date']

        medical_history_model = MedicalHistoryModel(mysql)
        # Validación: comprueba si la historia médica ya existe
        if medical_history_model.history_exists(history_id):
            return jsonify({
                'success': False,
                'message': 'La historia médica ya existe. Por favor verifique o ingrese otra.'
            }), 400

        # Si no existe, se procede a agregarla
        medical_history_model.add_medical_history(history_id, patient_id, doctor_id, diagnosis, observation, observation_date)
        return jsonify({'success': True, 'message': '¡Historia médica agregada exitosamente!'})
    else:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

@histories_bp.route('/update/<int:history_id>', methods=['POST'])
@login_required
def update_history(history_id):
    if 'rol' in session and session['rol'] == 'admin':
        diagnosis       = request.form['diagnosis']
        observation     = request.form['observation']
        observation_date= request.form['observation_date']

        medical_history_model = MedicalHistoryModel(mysql)
        medical_history_model.update_medical_history(history_id, diagnosis, observation, observation_date)

        return jsonify({'success': True, 'message': '¡Historia médica actualizada exitosamente!'})
    else:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

@histories_bp.route('/delete/<int:history_id>', methods=['POST'])
@login_required
def delete_history(history_id):
    if 'rol' in session and session['rol'] == 'admin':
        medical_history_model = MedicalHistoryModel(mysql)
        medical_history_model.delete_medical_history(history_id)

        return jsonify({'success': True, 'message': '¡Historia médica eliminada exitosamente!'})
    else:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403
