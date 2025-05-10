document.addEventListener('DOMContentLoaded', function() {
    // Profile Image Upload
    const editImageBtn = document.querySelector('.edit-image-btn');
    const imageUpload = document.getElementById('profile-image-upload');
    const profileImage = document.querySelector('.profile-image img');
    
    editImageBtn.addEventListener('click', function() {
        imageUpload.click();
    });
    
    imageUpload.addEventListener('change', function(e) {
        if (e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = function(event) {
                profileImage.src = event.target.result;
                // In a real app, you would upload the image to the server here
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    });
});

