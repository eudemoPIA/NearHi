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

function toggleFavorite(eventId) {  // the red heart for save event
    fetch(`/events/save/${eventId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(response => response.json())
    .then(data => {
        const heartIcon = document.querySelector('#favorite-button i');
        if (data.is_favorite) {
            heartIcon.classList.remove('far'); // solid heart
            heartIcon.classList.add('fas');
        } else {
            heartIcon.classList.remove('fas'); // empty heart
            heartIcon.classList.add('far');
        }
    });
}

function applyEvent(eventId) {
    // 获取按钮和参与人数的元素
    const applyButton = document.querySelector('#apply-button');
    const participantCountElement = document.querySelector('.current-participants');

    applyButton.addEventListener('click', function() {
        fetch(`/events/${eventId}/apply/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            // 动态更新参与人数和按钮状态
            participantCountElement.textContent = `Current Participants: ${data.current_participants}`;
            applyButton.textContent = data.applied ? 'Applied' : 'Apply';
        })
        .catch(error => console.error('Error:', error));
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const applyButton = document.querySelector('#apply-button');
    if (applyButton) {
        // 获取页面加载时确定的 eventId
        const eventId = applyButton.dataset.eventId;
        // 调用 applyEvent 进行事件绑定
        applyEvent(eventId);
    }
});

