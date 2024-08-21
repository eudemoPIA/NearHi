// 通用的确认弹窗函数
function showConfirmationModal(actionType, eventId, successCallback) {
    // 显示确认弹窗
    $('#confirmationModal').modal('show');

    // 当用户点击确认按钮时
    $('#confirmAction').off('click').on('click', function() {
        $.ajax({
            type: "POST",
            url: `/your-app/${actionType}/${eventId}/`,
            headers: {
                'X-CSRFToken': csrftoken, // 确保 CSRF token 被正确设置
            },
            success: function(response) {
                if (response.status === 'success') {
                    successCallback(); // 在成功后执行自定义操作，例如移除活动卡片
                    $('#confirmationModal').modal('hide'); // 关闭弹窗
                }
            },
            error: function() {
                alert('An error occurred, please try again.');
            }
        });
    });
}

// 绑定事件逻辑
$(document).ready(function() {
    $('.action-btn').on('click', function() {
        const actionType = $(this).data('action-type');
        const eventId = $(this).data('event-id');
        showConfirmationModal(actionType, eventId, function() {
            // 成功后移除对应的活动卡片
            $(`#event-card-${eventId}`).remove();
        });
    });
});
