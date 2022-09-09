from django.db import models

# Create your models here.
class Tasks(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    title = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=50)
