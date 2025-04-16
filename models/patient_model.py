class PatientModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_patient_by_id(self, patient_id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
        patient = cur.fetchone()
        cur.close()
        return patient    

    def get_all_patients(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT  patient_id, name, last_name, age, gender, birth_date, patient_record, diagnosis, created_at FROM patients")
        patients = cur.fetchall()
        cur.close()
        return patients

    def add_patient(self, patient_id, name, last_name, age, gender, birth_date, patient_record, diagnosis):
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO patients ( patient_id,name, last_name, age, gender, birth_date, patient_record, diagnosis, created_at) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, NOW())",
                    ( patient_id,name, last_name, age, gender, birth_date, patient_record, diagnosis))
        self.mysql.connection.commit()
        cur.close()
