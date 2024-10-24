from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10)  # Present/Absent

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.status}"


# Create your models here.
