from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

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

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=800)
    event_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # 费用字段，默认0
    max_participants = models.PositiveIntegerField(default=1)  # 最大参与人数
    current_participants = models.PositiveIntegerField(default=0, editable=False)  # 当前参与人数，自动更新

    def _str_(self):
        return self.title

# Create your models here.
