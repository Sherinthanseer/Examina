from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class ActivityLog(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the student user
    activity = models.TextField()  # Log the activity details
    timestamp = models.DateTimeField(default=now)  # Timestamp of the activity

    def __str__(self):
        return f"{self.student.username} - {self.activity} at {self.timestamp}"