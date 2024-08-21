document.addEventListener('DOMContentLoaded', function () {
    const sendCodeButton = document.getElementById('send-code');
    const countdownElement = document.getElementById('countdown');
    let countdown = 60; 
    let interval;

    sendCodeButton.addEventListener('click', function () {
        fetch('http://127.0.0.1:8000/send-code/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: document.querySelector('input[name="email"]').value
            })
        }).then(response => response.json()).then(data => {
            if (data.status === 'ok') {
                sendCodeButton.style.display = 'none';
                countdownElement.style.display = 'inline';
                countdownElement.textContent = `Resend in ${countdown}s`;

                interval = setInterval(() => {
                    countdown--;
                    if (countdown > 0) {
                        countdownElement.textContent = `Resend in ${countdown}s`;
                    } else {
                        clearInterval(interval);
                        sendCodeButton.style.display = 'inline'; 
                        countdownElement.style.display = 'none';
                        countdown = 60; 
                    }
                }, 1000);
            } else {
                alert(data.message);
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('Failed to send verification code. Please try again.');
        });
    });
});
