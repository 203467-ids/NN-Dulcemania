const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const captureButton = document.getElementById('capture');
const switchCameraButton = document.getElementById('switch-camera');
const switchCameraMessage = document.getElementById('switch-camera-message');
const resultsDiv = document.getElementById('results');

captureButton.addEventListener('click', () => {
    // Captura la imagen del video y la muestra en el canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convierte la imagen del canvas a base64
    const imageData = canvas.toDataURL('image/jpeg');

    // Envía la imagen al servidor para su procesamiento
    $.ajax({
        type: 'POST',
        url: '/predict',
        data: { image_data: imageData },
        success: function(response) {
            // Muestra los resultados de la predicción en la página
            resultsDiv.innerHTML = response.results;
        }
    });
});

// Abre la cámara del dispositivo móvil y muestra la transmisión en el elemento de video
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        console.error('Error accessing the camera: ', err);
        switchCameraMessage.style.display = 'block'; // Mostrar el mensaje de cambio de cámara
        switchCameraButton.style.display = 'block'; // Mostrar el botón de cambiar cámara
    });

// Cambiar manualmente entre las cámaras frontal y trasera al hacer clic en el botón
switchCameraButton.addEventListener('click', () => {
    switchCameraMessage.style.display = 'block'; // Mostrar el mensaje de cambio de cámara
});
