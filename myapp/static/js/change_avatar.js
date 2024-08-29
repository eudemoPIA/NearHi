/*
change profile picture and back to the default profile picture
*/

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('profile-picture-input');
    const removeAvatarButton = document.getElementById('remove-avatar');
    const profileImage = document.querySelector('.profile-picture-label img');

    if (fileInput) {
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    profileImage.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    if (removeAvatarButton) {
        removeAvatarButton.addEventListener('click', function() {
            profileImage.src = '/media/profile_pictures/default_avatar.png';
            fileInput.value = '';
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var removeAvatarButton = document.getElementById('remove-avatar');
    
    if (removeAvatarButton) {
        removeAvatarButton.addEventListener('click', function() {
            document.getElementById('remove_avatar_field').value = "true";  
        });
    }
});
