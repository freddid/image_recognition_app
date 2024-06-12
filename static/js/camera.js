const video = document.querySelector('#video');
const canvas = document.querySelector('#canvas');
const context = canvas.getContext('2d');
const captureButton = document.querySelector('#captureButton');
const uploadButton = document.querySelector('#uploadButton');

// Настройка веб-камеры
navigator.mediaDevices.getUserMedia({ video: true })
   .then(stream => {
      video.srcObject = stream;
   })
   .catch(err => {
      console.error("Ошибка доступа к веб-камере: ", err);
   });

// Захват изображения с веб-камеры
captureButton.addEventListener('click', () => {
   context.drawImage(video, 0, 0, canvas.width, canvas.height);
   const dataURL = canvas.toDataURL('image/png');
   document.querySelector('#capturedImage').src = dataURL;
   document.querySelector('#imageData').value = dataURL;
   uploadButton.style.display = 'inline';
});
