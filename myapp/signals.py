from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import Comment, Notification

from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import Comment, Notification, Event

@receiver(post_save, sender=Comment)
def notify_on_comment(sender, instance, created, **kwargs):
    if created:
        # 检查是否是回复
        if instance.parent:
            # 这是一条回复
            if instance.user == instance.event.created_by:
                # 如果回复者是事件的创建者
                Notification.objects.create(
                    recipient=instance.parent.user,  # 回复给原评论作者
                    message=f"The event creator replied to your comment on '{instance.event.title}'",
                    event=instance.event
                )
        else:
            # 这不是回复，是一条新评论
            if instance.user != instance.event.created_by:
                # 如果评论者不是事件的创建者
                Notification.objects.create(
                    recipient=instance.event.created_by,  # 通知事件的创建者
                    message=f"{instance.user.username} commented on your event '{instance.event.title}'",
                    event=instance.event
                )