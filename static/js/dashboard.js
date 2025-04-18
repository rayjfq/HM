function showModal(modalId) {
    document.getElementById(modalId).style.display = "flex";
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    const successMessage = modal.querySelector(".success-message");
    if (successMessage) successMessage.style.display = 'none';
    modal.style.display = 'none';
}

function configureForm(formId, url, modalId, successMessageId) {
    const form = document.getElementById(formId);
    if (!form) {
        console.error("No se encontró el formulario con id:", formId);
        return;
    }
    form.onsubmit = function (event) {
        event.preventDefault();

        fetch(url, {
            method: "POST",
            body: new FormData(event.target)
        })
        .then(response => {
            console.log("Response status:", response.status);
            if (response.ok) return response.json();
            else {
                return response.text().then(text => {
                    throw new Error(`Error al procesar la solicitud. Status ${response.status}. Respuesta: ${text}`);
                });
            }
            
        })
        .then(data => {
            if (data.success) {
                console.log("Éxito: se recibió data.success = true");
                const successMessage = document.getElementById(successMessageId);
                successMessage.textContent = data.message;
                successMessage.style.display = 'block';

                form.reset();

                setTimeout(() => {
                    console.log("Ejecutando redirección a /dashboard");
                    //closeModal(modalId);
                    window.location.href = '/dashboard';
                }, 2000);
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Hubo un error al procesar tu solicitud.");
        });
    };
}

// Esta función se llama una vez que los modales ya se han insertado en el DOM.
function initModalForms() {
    configureForm("create-user-form", "/create_user", "create-user-modal", "success-message-user");
    configureForm("create-history-form", "/histories/add", "create-history-modal", "success-message-history");
    configureForm("create-patient-form", "/patients/add", "add-patient-modal", "success-message-patient");
    configureForm("create-doctor-form", "/doctors/add", "add-doctor-modal", "success-message-doctor");
}
