/*
apply and save functions on event_detail page
*/

// if not autheticated, redirected to the login page
function handleResponse(response) {
    if (response.redirected) { 
        window.location.href = response.url; 
        return;
    }
    return response.json();
}

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

//the empty heart become solid when toggle the favorite button
function toggleFavorite(eventId) {  // the red heart for save event
    fetch(`/events/save/${eventId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(handleResponse)
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

//apply for some event with the increase of current participant increase and turning to 'Applied'
function applyEvent(eventId) {
    const applyButton = document.querySelector('#apply-button');
    const participantCountElement = document.querySelector('#participant-count');

    applyButton.addEventListener('click', function() {
        fetch(`/events/${eventId}/apply/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            }
        })
        .then(handleResponse)
        .then(data => {
            participantCountElement.textContent =  data.current_participants;
            applyButton.textContent = data.applied ? 'Applied' : 'Apply';
        })
        .catch(error => console.error('Error:', error));
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const applyButton = document.querySelector('#apply-button');
    if (applyButton) {
        const eventId = applyButton.dataset.eventId;
        applyEvent(eventId);
    }
});

