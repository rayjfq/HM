class DoctorModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_doctor_by_id(self, doctor_id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM doctors WHERE doctor_id = %s", (doctor_id,))
        doctor = cur.fetchone()
        cur.close()
        return doctor

    def get_all_doctors(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT doctor_id, name, last_name, title, email, specialty, created_at FROM doctors")
        doctors = cur.fetchall()
        cur.close()
        return doctors

    def add_doctor(self, doctor_id, name, last_name, title, email, specialty):
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO doctors (doctor_id,name, last_name, title, email, specialty, created_at) VALUES (%s,%s, %s, %s, %s, %s, NOW())",
                    (doctor_id,name, last_name, title, email, specialty))
        self.mysql.connection.commit()
        cur.close()
