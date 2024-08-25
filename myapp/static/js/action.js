console.log('action.js loaded');

// 获取 CSRF token 的函数
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

// 关闭模态框
function closeModal() {
    document.getElementById('confirmationModal').style.display = 'none';
}

// 更新参与者数量
function updateParticipantsCount(data) {
    const participantCountElement = document.getElementById('current-participants');
    if (participantCountElement) {
        participantCountElement.innerText = `${data.current_participants} participants`;
    } else {
        console.error('Element not found: participantCount');
    }
}

// 移除事件卡片
function removeEventCard(eventId) {
    const eventCard = document.getElementById(`event-card-${eventId}`);
    if (eventCard) {
        eventCard.remove();
        console.log(`Removed event card with ID: event-card-${eventId}`);
    } else {
        console.log(`No event card found with ID: event-card-${eventId}`);
    }
}

// 通用的确认弹窗函数
function showConfirmationModal(actionType, eventId, successCallback) {
    const url = `/events/${actionType}/${eventId}/`;

    // 显示模态框
    document.getElementById('confirmationModal').style.display = 'block';

    // 绑定关闭按钮事件
    document.getElementById('closeModal').onclick = closeModal;

    // 绑定确认按钮事件
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
                updateParticipantsCount(data); // 直接更新参与者数量
                successCallback(); // 执行成功后的回调
                closeModal(); // 关闭弹窗
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

// 绑定事件逻辑，使用事件委托
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('action-btn')) {
        console.log('Button clicked');
        const actionType = event.target.getAttribute('data-action-type');
        const eventId = event.target.getAttribute('data-event-id');
        showConfirmationModal(actionType, eventId, function() {
            removeEventCard(eventId); // 移除事件卡片
        });
    }
});
