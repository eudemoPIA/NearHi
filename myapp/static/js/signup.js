document.addEventListener('DOMContentLoaded', function () {
    const sendCodeButton = document.getElementById('send-code');
    const countdownElement = document.getElementById('countdown');
    let countdown = 60; 
    let interval;

    sendCodeButton.addEventListener('click', function () {
        fetch("{% url 'send_verification_code' %}", {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: document.querySelector('input[name="email"]').value
            })
        }).then(response => response.json()).then(data => {
            if (data.status === 'ok') {
                sendCodeButton.disabled = true;
                countdownElement.textContent = `Resend in ${countdown}s`;
                interval = setInterval(() => {
                    countdown--;
                    if (countdown > 0) {
                        countdownElement.textContent = `Resend in ${countdown}s`;
                    } else {
                        clearInterval(interval);
                        sendCodeButton.disabled = false;
                        countdownElement.textContent = '';
                        countdown = 60; 
                    }
                }, 1000);
            } else {
                alert(data.message);
            }
        });
    });
});
