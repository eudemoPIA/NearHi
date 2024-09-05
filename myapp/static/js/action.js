/*
confirm popups for 'delete' in my_events, 'unfavorite' in saved_events and 'cancel application' in upcoming_events
*/

// acquire CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// close the modal
function closeModal() {
    document.getElementById('confirmationModal').style.display = 'none';
}



// remove the event card
function removeEventCard(eventId) {
    const eventCard = document.getElementById(`event-card-${eventId}`);
    if (eventCard) {
        eventCard.remove();
        console.log(`Removed event card with ID: event-card-${eventId}`);
    } else {
        console.log(`No event card found with ID: event-card-${eventId}`);
    }
}

// commonly used confirm popups
function showConfirmationModal(actionType, eventId, successCallback) {
    const url = `/events/${actionType}/${eventId}/`;

    document.getElementById('confirmationModal').style.display = 'block';

    document.getElementById('closeModal').onclick = closeModal;

    document.getElementById('confirmAction').onclick = function() {
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log("data:::", data);

            if (data.status === 'success') {
                console.log('Updating participants...');
                updateParticipantsCount(data);
                successCallback();
                closeModal();
            } else {
                alert('An error occurred, please try again.');
            }
        })
        .catch(error => {
            console.log(error);
            alert('An error occurred, please try again.');
        });
    };
}


document.addEventListener('click', function(event) {
    if (event.target.classList.contains('action-btn')) {
        console.log('Button clicked');
        const actionType = event.target.getAttribute('data-action-type');
        const eventId = event.target.getAttribute('data-event-id');
        showConfirmationModal(actionType, eventId, function() {
            removeEventCard(eventId);
        });
    }
});

