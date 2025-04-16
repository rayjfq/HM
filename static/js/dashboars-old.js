function showModal(modalId) {
    document.getElementById(modalId).style.display = "flex";
}

// Función genérica para cerrar cualquier modal
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    const successMessage = modal.querySelector(".success-message");
    // Limpia el mensaje de éxito si existe
    if (successMessage) successMessage.style.display = 'none';
    // Oculta el modal
    modal.style.display = 'none';
}
function configureForm(formId, url, modalId, successMessageId) {
    const form = document.getElementById(formId);
    form.onsubmit = function (event) {
        event.preventDefault(); // Evita la recarga automática de la página

        fetch(url, {
            method: "POST",
            body: new FormData(event.target)
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error("Error al procesar la solicitud.");
            }
        })
        .then(data => {
            if (data.success) {
                console.log("Éxito: se recibió data.success = true");
                const successMessage = document.getElementById(successMessageId);
                successMessage.textContent = data.message; // Inserta el mensaje del servidor
                successMessage.style.display = 'block'; // Muestra el mensaje de éxito

                form.reset(); // Limpia los campos del formulario

                // Después de 2 segundos, cierra el modal y redirige al dashboard
                setTimeout(() => {
                    console.log("Ejecutando redirección a /dashboard");
                    closeModal(modalId); // Cierra el modal
                    window.location.href = '/dashboard'; // Redirige al dashboard
                }, 2000);
            } else {
                alert(data.message); // Maneja el mensaje de error
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Hubo un error al procesar tu solicitud.");
        });
    };
}
// Configurar los formularios para agregar usuarios, historia, paciente y médico
configureForm("create-user-form", "/create_user", "create-user-modal", "success-message-user");
configureForm("create-history-form", "/add_history", "create-history-modal", "success-message-history");
configureForm("create-patient-form", "/add_patient", "add-patient-modal", "success-message-patient");
configureForm("create-doctor-form", "/add_doctor", "add-doctor-modal", "success-message-doctor");
