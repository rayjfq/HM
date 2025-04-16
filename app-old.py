from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from models.user_model import UserModel
from models.patient_model import PatientModel
from models.doctor_model import DoctorModel
from models.medical_history_model import MedicalHistoryModel
from models.observation_model import ObservationModel

app = Flask(__name__)
app.config.from_object('config.Config')

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, password_hash,rol FROM users WHERE id = %s", (user_id,))
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Variable para almacenar el mensaje de error
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Busca al usuario en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, email, password_hash, rol FROM users WHERE username = %s", (username,))
        user_data = cur.fetchone()
        cur.close()
       
        # Verifica si el usuario y contraseña son válidos
        if user_data and bcrypt.check_password_hash(user_data[3], password):
            user = User()
            user.id = user_data[0]
            session['rol'] = user_data[4]  # Guarda el rol en la sesión
            session['username'] = user_data[1]  # Guarda el nombre de usuario en la sesión
          
            login_user(user)  # Inicia sesión con Flask-Login
            return redirect(url_for('dashboard'))
        else:
            # Si las credenciales son incorrectas, asigna un mensaje de error
            error = "Usuario o contraseña incorrectos. Por favor, verifica tus datos e inténtalo nuevamente."
            
    
    # Renderiza el formulario de login con el mensaje de error (si existe)
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Cierra sesión usando Flask-Login
    session.clear()  # Limpia la sesión
    return redirect(url_for('login'))  # Redirige al login

@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    # Verifica si el rol es 'admin'
    if 'rol' in session and session['rol'] == 'admin':
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            rol = request.form['rol']  # Selecciona el rol del nuevo usuario
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            # Inserta al nuevo usuario en la base de datos
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, email, password_hash, rol) VALUES (%s, %s, %s, %s)", 
                        (username, email, hashed_password, rol))
            mysql.connection.commit()
            cur.close()
            return jsonify({'success': True, 'message': '¡Usuario agregado satisfactoriamente!'})
            #flash('¡Usuario agregado satisfactoriamente!')
            #return redirect(url_for('dashboard'))  # Redirige al dashboard después de crear el usuario
        
        return render_template('create_user.html')  # Muestra el formulario para crear usuarios
    else:
        #flash('No tienes permisos para realizar esta acción.', 'error')
        #return "Acceso no autorizado", 403  # Mensaje si el rol no es admin
        return jsonify({'success': False, 'message': 'No tienes permisos para realizar esta acción.'}), 403
    
@app.route('/list_users')
@login_required
def list_users():
    # Verifica que el usuario tenga el rol de admin
    if 'rol' in session and session['rol'] == 'admin':
        user_model = UserModel(mysql)  # Crea una instancia del modelo
        users = user_model.get_all_users()  # Obtiene la lista de usuarios
        return render_template('list_users.html', users=users)  # Pasa los datos a la plantilla
    else:
        return "Acceso no autorizado", 403  # Mensaje si el rol no es admin

has_initialized = False
@app.before_request
def initialize():
    global has_initialized
    if not has_initialized:
        create_admin_user()
        has_initialized = True

def create_admin_user():
    cur = mysql.connection.cursor()
    hashed_password = bcrypt.generate_password_hash('15111974').decode('utf-8')
    try:
        cur.execute("SELECT id FROM users WHERE username = 'admin'")
        if cur.fetchone() is None:
            cur.execute("INSERT INTO users (username, email, password_hash, rol) VALUES (%s, %s, %s, %s)", 
                        ('admin', 'admin@ucim.com', hashed_password,'admin'))
            mysql.connection.commit()
            print("Superusuario creado con éxito")
        else:
            print("El superusuario ya existe")
    except Exception as e:
        print(f"Error al crear el superusuario: {e}")
    finally:
        cur.close()

@app.route('/list_patients')
@login_required
def list_patients():
    patient_model = PatientModel(mysql)
    patients = patient_model.get_all_patients()
    return render_template('list_patients.html', patients=patients)

@app.route('/add_patient', methods=['POST'])
@login_required
def add_patient():
    if 'rol' in session and session['rol'] == 'admin':
        patient_id = request.form['patient_id']
        name = request.form['name']
        last_name = request.form['last_name']
        age = request.form['age']
        gender = request.form['gender']
        birth_date = request.form['birth_date']
        patient_record = request.form['patient_record']
        diagnosis = request.form['diagnosis']

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

@app.route('/list_doctors')
@login_required
def list_doctors():
    doctor_model = DoctorModel(mysql)
    doctors = doctor_model.get_all_doctors()
    return render_template('list_doctors.html', doctors=doctors)

@app.route('/add_doctor', methods=['POST'])
@login_required
def add_doctor():
    if 'rol' in session and session['rol'] == 'admin':
        doctor_id = request.form['doctor_id']
        name = request.form['name']
        last_name = request.form['last_name']
        title = request.form['title']
        email = request.form['email']
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

    
@app.route('/list_history')
@login_required
def list_history():
    medical_history_model= MedicalHistoryModel(mysql)
    histories = medical_history_model.get_all_histories()
    return render_template('list_history.html', histories=histories)    

@app.route('/add_history', methods=['POST'])
@login_required
def add_history():
    if 'rol' in session and session['rol'] == 'admin':
        history_id = request.form['history_id']
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        diagnosis = request.form['diagnosis']
        observation = request.form['observation']
        observation_date = request.form['observation_date']

        medical_history_model = MedicalHistoryModel(mysql)
        # Validación: comprueba si la historia médica ya existe
        if medical_history_model.history_exists(history_id):
            return jsonify({
                'success': False,
                'message': 'La historia médica ya existe. Por favor verifique o ingrese otra.'
            }), 400
        # Si no existe, se procede a agregarlo
        medical_history_model.add_medical_history(history_id,patient_id, doctor_id, diagnosis, observation, observation_date)
        return jsonify({'success': True, 'message': '¡Historia médica agregada exitosamente!'})
    else:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

@app.route('/update_history/<int:history_id>', methods=['POST'])
@login_required
def update_history(history_id):
    if 'rol' in session and session['rol'] == 'admin':
        diagnosis = request.form['diagnosis']
        observation = request.form['observation']
        observation_date = request.form['observation_date']

        medical_history_model = MedicalHistoryModel(mysql)
        medical_history_model.update_medical_history(history_id, diagnosis, observation, observation_date)

        return jsonify({'success': True, 'message': '¡Historia médica actualizada exitosamente!'})
    else:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

@app.route('/delete_history/<int:history_id>', methods=['POST'])
@login_required
def delete_history(history_id):
    if 'rol' in session and session['rol'] == 'admin':
        medical_history_model = MedicalHistoryModel(mysql)
        medical_history_model.delete_medical_history(history_id)

        return jsonify({'success': True, 'message': '¡Historia médica eliminada exitosamente!'})
    else:
        return jsonify({'success': False, 'message': 'Acceso no autorizado.'}), 403

@app.route('/add_observation', methods=['POST'])
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

@app.route('/get_observations/<string:patient_id>/<string:doctor_id>')
@login_required
def get_observations(patient_id, doctor_id):
    observation_model = ObservationModel(mysql)
    observations = observation_model.get_observations_by_history(patient_id, doctor_id)
    return jsonify(observations)

@app.route('/update_observation/<int:observation_id>', methods=['POST'])
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

@app.route('/buscarhistory')
@login_required
def buscar_history():
    return render_template('buscarhistory.html')

@app.route('/get_patient_data/<string:patient_id>')
@login_required
def get_patient_data(patient_id):
    try:
        # Obtener datos del paciente
        cur = mysql.connection.cursor()
        cur.execute("SELECT name, last_name, gender, birth_date FROM patients WHERE id = %s", (patient_id,))
        patient = cur.fetchone()

        if not patient:
            return jsonify({'success': False, 'message': 'Paciente no encontrado.'})

        # Obtener datos del médico asociado
        cur.execute("""
            SELECT d.name, d.last_name, d.specialty 
            FROM doctors d
            JOIN medical_histories mh ON mh.doctor_id = d.id
            WHERE mh.patient_id = %s
            LIMIT 1
        """, (patient_id,))
        doctor = cur.fetchone()

        # Obtener observaciones
        cur.execute("""
            SELECT observation_text, date 
            FROM observations 
            WHERE patient_id = %s
            ORDER BY date DESC
        """, (patient_id,))
        observations = cur.fetchall()
        cur.close()

        # Formatear los resultados
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

@app.route('/admin')
@login_required
def admin_dashboard():
    if session.get('rol') != 'admin':
        return "Acceso no autorizado", 403
    return render_template('admin_dashboard.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if 'rol' not in session or session['rol'] != 'admin':
        return "Acceso no autorizado", 403
    return render_template('dashboard.html')

@app.route('/')
def home():
    if 'username' in session:  # Si el usuario ya está autenticado
        return redirect(url_for('dashboard'))  # Redirige al dashboard
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


