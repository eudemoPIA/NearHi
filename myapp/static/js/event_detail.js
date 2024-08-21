function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggleFavorite(eventId) {  // 专门处理前端的 AJAX 请求的url,待配置
    fetch(`/toggle-favorite/${eventId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(response => response.json())
    .then(data => {
        const heartIcon = document.querySelector('#favorite-button i');
        if (data.is_favorite) {
            heartIcon.classList.remove('far'); // 切换到实心
            heartIcon.classList.add('fas');
        } else {
            heartIcon.classList.remove('fas'); // 切换到空心
            heartIcon.classList.add('far');
        }
    });
}

function applyEvent(eventId) {
    fetch(`/apply-event/${eventId}/`, {   //apply event的url(这个event_detail还得配个url，带着event/<int:event_id>/的)
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(response => response.json())
    .then(data => {
        const applyButton = document.querySelector('#apply-button');
        if (data.applied) {
            applyButton.innerText = 'Applied';
        } else {
            applyButton.innerText = 'Apply';
        }
    });
}
