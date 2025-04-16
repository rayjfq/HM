class MedicalHistoryModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def history_exists(self, history_id):
        """
        Verifica si una historia médica ya existe por su history_id.
        Retorna True si existe, de lo contrario False.
        """
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT history_id FROM medical_histories WHERE history_id = %s", (history_id,))
        exists = cur.fetchone() is not None
        cur.close()
        return exists

    def get_all_histories(self):
        """Obtiene todas las historias médicas."""
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT history_id, patient_id, doctor_id, diagnosis, observation, observation_date, created_at, updated_at FROM medical_histories")
        histories = cur.fetchall()
        cur.close()
        return histories

    def get_history_by_id(self, history_id):
        """Obtiene una historia médica por su ID."""
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT history_id, patient_id, doctor_id, diagnosis, observation, observation_date, created_at, updated_at FROM medical_histories WHERE id = %s", (history_id,))
        history = cur.fetchone()
        cur.close()
        return history

    def add_medical_history(self, history_id, patient_id, doctor_id, diagnosis, observation, observation_date):
        """Agrega una nueva historia médica."""
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO medical_histories (patient_id, doctor_id, diagnosis, observation, observation_date, created_at) VALUES (%s, %s, %s, %s, %s, NOW())",
                    (history_id, patient_id, doctor_id, diagnosis, observation, observation_date))
        self.mysql.connection.commit()
        cur.close()

    def update_medical_history(self, history_id, diagnosis, observation, observation_date):
        """Actualiza una historia médica existente."""
        cur = self.mysql.connection.cursor()
        cur.execute("UPDATE medical_histories SET diagnosis = %s, observation = %s, observation_date = %s, updated_at = NOW() WHERE id = %s",
                    (diagnosis, observation, observation_date, history_id))
        self.mysql.connection.commit()
        cur.close()

    def delete_medical_history(self, history_id):
        """Elimina una historia médica por su ID."""
        cur = self.mysql.connection.cursor()
        cur.execute("DELETE FROM medical_histories WHERE id = %s", (history_id,))
        self.mysql.connection.commit()
        cur.close()
