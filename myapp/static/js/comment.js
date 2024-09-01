document.addEventListener('DOMContentLoaded', function () {
    const commentForm = document.getElementById('comment-form');
    if (commentForm) {
        commentForm.addEventListener('submit', function (e) {
            e.preventDefault(); 

            const content = document.querySelector('textarea[name="content"]').value;
            const eventId = document.getElementById('apply-button').dataset.eventId;
            const parentCommentId = document.getElementById('parent_id_field').value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/events/${eventId}/add_comment/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ content: content, parent_id: parentCommentId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    addCommentToList(data);
                    document.querySelector('textarea[name="content"]').value = '';
                    document.getElementById('parent_id_field').value = ''; 
                } else {
                    console.error('Error adding comment:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    bindReplyButtons();
});

function bindReplyButtons() {
    document.querySelectorAll('.reply-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault(); 
            const commentId = this.getAttribute('data-comment-id');
            const parentComment = this.closest('.comment-item');
            document.getElementById('parent_id_field').value = commentId;

            
            if (parentComment.querySelector('.reply-form')) {
                return;
            }

            const replyForm = document.createElement('form');
            replyForm.className = 'reply-form';
            replyForm.innerHTML = `
                <textarea name="reply_content" placeholder="Write your reply..." required></textarea>
                <button type="submit" class="btn btn-primary">Add Reply</button>
            `;

            parentComment.appendChild(replyForm);

            replyForm.addEventListener('submit', function (e) {
                e.preventDefault(); 

                const content = replyForm.querySelector('textarea[name="reply_content"]').value;
                const eventId = document.getElementById('apply-button').dataset.eventId; 
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                fetch(`/events/${eventId}/add_comment/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({ content: content, parent_id: commentId })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        addReplyToComment(data, parentComment);
                        replyForm.remove();
                    } else {
                        console.error('Error adding reply:', data.message);
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });
    });
}

function addCommentToList(commentData) {
    const commentsList = document.querySelector('.comments-list');
    const newComment = document.createElement('li');
    newComment.className = 'comment-item';
    newComment.setAttribute('data-comment-id', commentData.comment_id);
    newComment.innerHTML = `
        <div class="comment-header">
            <strong>${commentData.user}</strong>
            <small>${commentData.created_at}</small>
        </div>
        <p>${commentData.comment}</p>
    `;
    if (commentData.is_reply) {
        const parentComment = document.querySelector(`.comment-item[data-comment-id="${commentData.parent_id}"]`);
        if (parentComment) {
            addReplyToComment(commentData, parentComment);
        } else {
            commentsList.insertBefore(newComment, commentsList.firstChild);
        }
    } else {
        commentsList.insertBefore(newComment, commentsList.firstChild);
    }
    bindReplyButtons();
}

function addReplyToComment(replyData, parentComment) {
    let repliesList = parentComment.querySelector('.replies-list');
    if (!repliesList) {
        repliesList = document.createElement('ul');
        repliesList.className = 'replies-list';
        parentComment.appendChild(repliesList);
    }
    const newReply = document.createElement('li');
    newReply.className = 'reply-comment';
    newReply.innerHTML = `
        <div class="comment-header">
            <strong>${replyData.user}</strong>
            <small>${replyData.created_at}</small>
        </div>
        <p>${replyData.comment}</p>
    `;
    repliesList.appendChild(newReply);
}

