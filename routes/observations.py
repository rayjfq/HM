from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required
from models.observation_model import ObservationModel
#from app import mysql  # Asegúrate de que 'mysql' se haya inicializado y exportado en tu app principal
from extensions import mysql, bcrypt, login_manager 

observations_bp = Blueprint('observations', __name__, url_prefix='/observations')

# Endpoint para agregar una observación
@observations_bp.route('/add', methods=['POST'])
@login_required
def add_observation():
    if 'rol' in session and session['rol'] == 'medico':
        patient_id = request.form['patient_id']
        doctor_id = session['user_id']  # ID del médico conectado
        observation_text = request.form['observation_text']
        date = request.form['date']

        observation_model = ObservationModel(mysql)
        observation_model.add_observation(patient_id, doctor_id, observation_text, date)

        return jsonify({'success': True, 'message': '¡Observación agregada exitosamente!'})
    else:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

# Endpoint para obtener las observaciones según el paciente y el médico
@observations_bp.route('/get/<string:patient_id>/<string:doctor_id>')
@login_required
def get_observations(patient_id, doctor_id):
    observation_model = ObservationModel(mysql)
    observations = observation_model.get_observations_by_history(patient_id, doctor_id)
    return jsonify(observations)

# Endpoint para actualizar una observación
@observations_bp.route('/update/<int:observation_id>', methods=['POST'])
@login_required
def update_observation(observation_id):
    if 'rol' in session and session['rol'] == 'medico':
        observation_text = request.form['observation_text']
        date = request.form['date']

        observation_model = ObservationModel(mysql)
        observation_model.update_observation(observation_id, observation_text, date)

        return jsonify({'success': True, 'message': '¡Observación actualizada exitosamente!'})
    else:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

# Endpoint para mostrar la interfaz de búsqueda de historias
@observations_bp.route('/buscarhistory')
@login_required
def buscar_history():
    return render_template('buscarhistory.html')

# Endpoint para obtener datos de un paciente, su médico asociado y observaciones 
@observations_bp.route('/get_patient_data/<string:patient_id>')
@login_required
def get_patient_data(patient_id):
    try:
        # Obtener datos del paciente
        cur = mysql.connection.cursor()
        cur.execute("SELECT name, last_name, gender, birth_date FROM patients WHERE id = %s", (patient_id,))
        patient = cur.fetchone()

        if not patient:
            return jsonify({'success': False, 'message': 'Paciente no encontrado.'})

        # Obtener datos del médico asociado (se toma el primer registro relacionado)
        cur.execute("""
            SELECT d.name, d.last_name, d.specialty 
            FROM doctors d
            JOIN medical_histories mh ON mh.doctor_id = d.id
            WHERE mh.patient_id = %s
            LIMIT 1
        """, (patient_id,))
        doctor = cur.fetchone()

        # Obtener observaciones del paciente
        cur.execute("""
            SELECT observation_text, date 
            FROM observations 
            WHERE patient_id = %s
            ORDER BY date DESC
        """, (patient_id,))
        observations = cur.fetchall()
        cur.close()

        return jsonify({
            'success': True,
            'patient': {
                'name': patient[0],
                'last_name': patient[1],
                'gender': patient[2],
                'birth_date': patient[3],
            },
            'doctor': {
                'name': doctor[0] if doctor else "N/A",
                'last_name': doctor[1] if doctor else "N/A",
                'specialty': doctor[2] if doctor else "N/A",
            },
            'observations': [{'observation_text': o[0], 'date': o[1]} for o in observations]
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Error interno del servidor.'}), 500
