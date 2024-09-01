
document.addEventListener('DOMContentLoaded', function () {
    // Ensure notification dropdown is hidden initially
    const dropdown = document.getElementById('notification-dropdown');
    dropdown.style.display = 'none'; // Ensure it's hidden by default

    // 1. Get CSRF token
    const csrfTokenElement = document.getElementById('csrf-token');
    const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;

    // 2. Bind comment form submission event
    const commentForm = document.getElementById('comment-form');
    if (commentForm) {
        commentForm.addEventListener('submit', function (e) {
            e.preventDefault(); // Prevent default form submission
            handleCommentSubmit(csrfToken); // Implement this function according to your comment logic
        });
    }

    // 3. Bind reply button events
    if (typeof bindReplyButtons === 'function') {
        bindReplyButtons(); // Ensure bindReplyButtons() function is defined in your script
    } else {
        console.warn('bindReplyButtons function is not available.');
    }

    // 4. Bind notification icon click event
    const notificationIcon = document.querySelector('.notification-icon');
    if (notificationIcon) {
        notificationIcon.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleDropdown();
        });
    }

    // 5. Click on other place to close the dropdown
    document.addEventListener('click', function (e) {
        if (dropdown && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
    fetchNotifications();
});

// 6. Toggle notification dropdown visibility
function toggleDropdown() {
    const dropdown = document.getElementById('notification-dropdown');
    console.log('Toggling dropdown:', dropdown); // Debug info

    dropdown.style.display = ''; 
    
    if (dropdown.style.display === 'block') {
        console.log('Dropdown is active, hiding.'); // Debug when hiding
        dropdown.style.display = 'none'; // Explicitly hide the dropdown
    } else {
        console.log('Dropdown is not active, showing.'); // Debug when showing
        dropdown.style.display = 'block'; // Explicitly show the dropdown
        fetchNotifications(); // Fetch notifications when the dropdown becomes visible
    }
}
    
    
// 7. Fetch notifications logic
function fetchNotifications() {
    fetch('/notifications/')
        .then(response => response.json())
        .then(data => {
            console.log('Fetched notifications:', data.notifications); // Debug info
            displayNotifications(data.notifications); // Display fetched notifications
            updateNotificationIndicator(data.unread_count);
        })
        .catch(error => console.error('Error fetching notifications:', error));
}

// 8. Display notifications
function displayNotifications(notifications) {
    const dropdown = document.getElementById('notification-dropdown');
    dropdown.innerHTML = ''; // 清空现有通知内容

    if (notifications.length === 0) {
        dropdown.innerHTML = '<p>No new notifications.</p>';
        return;
    }

    notifications.forEach(notification => {
        const notificationElement = document.createElement('div');
        notificationElement.id = `notification-${notification.id}`; // Set an ID for each notification
        notificationElement.className = 'notification-item';
        notificationElement.innerHTML = `
            <a href="${notification.url}" class="notification-link" onclick="markNotificationAsRead(${notification.id}, event)">${notification.message}</a>
            <span class="dot"></span>
        `;
        dropdown.appendChild(notificationElement);
    });
}

// 9. Read and remove notifications
function markNotificationAsRead(notificationId, event) {
    const csrfTokenElement = document.getElementById('csrf-token');
    const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;

    
    fetch(`/mark_notification_as_read/${notificationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            const notificationElement = document.getElementById(`notification-${notificationId}`);
            if (notificationElement) {
                notificationElement.remove();
            }
            window.location.href = event.target.href;
        } else {
            throw new Error('Failed to mark notification as read.');
        }
    })
    .catch(error => console.error('Error marking notification as read:', error));
}

// 10. display whether there are unread notifications
function updateNotificationIndicator(count) {
    const notificationDot = document.getElementById('notification-dot');
    notificationDot.style.display = count > 0 ? 'block' : 'none';
}


