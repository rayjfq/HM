class ObservationModel:
    def __init__(self, mysql):
        self.mysql = mysql

    def get_all_observations(self):
        """Obtiene todas las observaciones."""
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT id, patient_id, doctor_id, observation_text, date, created_at, updated_at FROM observations")
        observations = cur.fetchall()
        cur.close()
        return observations

    def get_observations_by_history(self, patient_id, doctor_id):
        """Obtiene todas las observaciones relacionadas con una historia médica específica."""
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT id, observation_text, date, created_at, updated_at FROM observations WHERE patient_id = %s AND doctor_id = %s ORDER BY date DESC",
                    (patient_id, doctor_id))
        observations = cur.fetchall()
        cur.close()
        return observations

    def add_observation(self, patient_id, doctor_id, observation_text, date):
        """Agrega una nueva observación."""
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO observations (patient_id, doctor_id, observation_text, date, created_at) VALUES (%s, %s, %s, %s, NOW())",
                    (patient_id, doctor_id, observation_text, date))
        self.mysql.connection.commit()
        cur.close()

    def update_observation(self, observation_id, observation_text, date):
        """Actualiza una observación existente."""
        cur = self.mysql.connection.cursor()
        cur.execute("UPDATE observations SET observation_text = %s, date = %s, updated_at = NOW() WHERE id = %s",
                    (observation_text, date, observation_id))
        self.mysql.connection.commit()
        cur.close()

    def delete_observation(self, observation_id):
        """Elimina una observación por su ID."""
        cur = self.mysql.connection.cursor()
        cur.execute("DELETE FROM observations WHERE id = %s", (observation_id,))
        self.mysql.connection.commit()
        cur.close()
