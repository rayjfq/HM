
    function showModal() {
       document.getElementById("create-user-modal").style.display = "flex";
   }

   document.getElementById('create-user-modal').onsubmit = function(event) {
    event.preventDefault(); // Evita la recarga automática de la página

    fetch('/create_user', {
        method: 'POST',
        body: new FormData(event.target)
    })
    .then(response => {
        if (response.ok) { // Verifica si la respuesta del servidor es exitosa
            return response.json();
        } else {
            throw new Error('Error al procesar la solicitud.');
        }
    })
    .then(data => {
        if (data.success) {
            // Mostrar el mensaje de éxito en el modal
            const successMessage = document.getElementById('success-message');
            successMessage.textContent = data.message; // Inserta el mensaje del servidor
            successMessage.style.display = 'block'; // Muestra el mensaje

            // Limpia el formulario
            event.target.reset();

            // Después de 2 segundos, cierra el modal y redirige al dashboard
            setTimeout(() => {
                closeModal(); // Cierra el modal
                window.location.href = '/dashboard'; // Redirige al dashboard
            }, 2000);
        } else {
            alert(data.message); // Maneja el error si no se agregó correctamente
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error al procesar tu solicitud.');
    });
};

   function closeModal() {
    const modal = document.getElementById("create-user-modal");
    const successMessage = document.getElementById("success-message");
    // Limpia el mensaje de éxito
    successMessage.style.display = 'none';
    // Oculta el modal
    modal.style.display = 'none';
   }
 
