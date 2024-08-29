/*
show the password when needed
*/

document.addEventListener('DOMContentLoaded', function () {
    const showHidePw = document.querySelectorAll('.showHidePw');
    const passwordFields = document.querySelectorAll('.password');

    showHidePw.forEach((eyeIcon, index) => {
        eyeIcon.addEventListener('click', () => {
            const passwordField = passwordFields[index];
            if (passwordField.type === "password") {
                passwordField.type = "text";
                eyeIcon.classList.replace("uil-eye-slash", "uil-eye");
            } else {
                passwordField.type = "password";
                eyeIcon.classList.replace("uil-eye", "uil-eye-slash");
            }
        });
    });
});
