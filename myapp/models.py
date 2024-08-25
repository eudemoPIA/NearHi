from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default_avatar.png')
    city = models.CharField(max_length=100, null=True, blank=True)
    hobbies = models.CharField(max_length=255, blank=True)
    saved_events = models.ManyToManyField('Event', related_name='saved_by_users', blank=True)
    upcoming_events = models.ManyToManyField('Event', related_name='applied_by_users', blank=True)


class Event(models.Model):
    CATEGORY_CHOICES = [
        ('game', 'Game'),
        ('performance', 'Performance'),
        ('nature', 'Nature'),
        ('pet', 'Pet'),
        ('gourmet', 'Gourmet'),
        ('reading', 'Reading'),
        ('music', 'Music'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=800)
    event_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # 费用字段，默认0
    max_participants = models.PositiveIntegerField(default=1)  # 最大参与人数
    current_participants = models.PositiveIntegerField(default=0, editable=False)  # 当前参与人数，自动更新

    def __str__(self):
        return self.title
    
    def update_current_participants(self):
        self.current_participants = self.applied_by_users.count()
        self.save()
    
    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"pk": self.pk})
    

# Create your models here.
