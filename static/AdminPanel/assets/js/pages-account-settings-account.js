document.addEventListener('DOMContentLoaded', function () {
    for (let i = 1; i <= 5; i++) {
        const resetButton = document.getElementById('resetButton' + i);
        const accountUserImage = document.getElementById('uploadedAvatar' + i);
        const fileInput = document.getElementById('upload' + i);

        if (resetButton && accountUserImage && fileInput) {
            const resetImage = accountUserImage.src;
            fileInput.addEventListener('change', function () {
                if (fileInput.files[0]) {
                    accountUserImage.src = window.URL.createObjectURL(fileInput.files[0]);
                }
            });

            resetButton.addEventListener('click', function () {
                fileInput.value = '';
                accountUserImage.src = resetImage;
            });
        }
    }
});
