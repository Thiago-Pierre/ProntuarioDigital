document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    M.Modal.init(elems);

    // Função para lidar com a submissão do formulário de edição
    var editForms = document.querySelectorAll('.edit-form');
    editForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            var formData = new FormData(this);
            var pacienteId = this.id.replace('editForm', '');
            fetch('/api/editar/' + pacienteId, {
                method: 'POST',
                body: JSON.stringify(Object.fromEntries(formData.entries())),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                    window.location.reload(); // Recarrega a página para atualizar os dados
                } else {
                    alert('Erro ao atualizar os dados');
                }
            })
            .catch(error => {
                console.error('Erro ao atualizar os dados:', error);
            });
        });
    });

    // Função para lidar com a submissão do formulário de upload de fotos
    var uploadForms = document.querySelectorAll('.upload-form');
    uploadForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            var formData = new FormData(this);
            var pacienteId = this.id.replace('uploadForm', '');
            fetch('/api/upload/' + pacienteId, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert('Foto adicionada com sucesso!');
                    window.location.reload(); // Recarrega a página para atualizar as fotos
                } else {
                    alert('Erro ao adicionar foto');
                }
            })
            .catch(error => {
                console.error('Erro ao adicionar foto:', error);
            });
        });
    });

    // Função para inicializar a câmera e capturar a imagem
    var cameraModals = document.querySelectorAll('.camera-modal');
    cameraModals.forEach(function(modal) {
        var pacienteId = modal.id.replace('cameraModal', '');
        var video = document.getElementById('video' + pacienteId);
        var canvas = document.getElementById('canvas' + pacienteId);
        var captureButton = document.getElementById('capture' + pacienteId);
        var fileInput = document.getElementById('file' + pacienteId);

        // Inicializar a câmera quando o modal for aberto
        var modalInstance = M.Modal.getInstance(modal);
        modalInstance.options.onOpenStart = function() {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function(stream) {
                    video.srcObject = stream;
                })
                .catch(function(err) {
                    console.error('Erro ao acessar a câmera: ', err);
                });
        };

        captureButton.addEventListener('click', function() {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
            canvas.toBlob(function(blob) {
                var file = new File([blob], 'captured_photo.jpg', { type: 'image/jpeg' });
                var dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                fileInput.files = dataTransfer.files;

                // Corrigir o caminho da imagem
                var filePath = file.name.replace(/\\/g, '/');
                var inputField = document.querySelector('.file-path.validate');
                inputField.value = filePath;

                // Fechar o modal da câmera e retornar ao modal anterior
                M.Modal.getInstance(modal).close();
            });
        });
    });
});
