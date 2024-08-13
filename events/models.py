from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=200)
    time = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField(max_length=800)

    def __str__(self):
        return self.name
