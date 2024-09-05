from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import Comment, Notification

from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import Comment, Notification, Event

# two situations be notified
# 1. creator gets a new comment from other users
# 2. some user gets a reply from the event creator

@receiver(post_save, sender=Comment)
def notify_on_comment(sender, instance, created, **kwargs):
    if created:
        # check if it is a reply or not
        if instance.parent:
            # it is a reply
            if instance.user == instance.event.created_by:
                # if it is from the event creator
                Notification.objects.create(
                    recipient=instance.parent.user,  
                    message=f"The event creator replied to your comment on '{instance.event.title}'",
                    event=instance.event
                )
        else:
            # it is a new comment
            if instance.user != instance.event.created_by:
                # if it is not from the event creator
                Notification.objects.create(
                    recipient=instance.event.created_by,  # notify the event creator
                    message=f"{instance.user.username} commented on your event '{instance.event.title}'",
                    event=instance.event
                )