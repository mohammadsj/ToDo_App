from django.db import models
<<<<<<< Updated upstream
from django.contrib.auth.models import User
=======
from django.contrib.auth import get_user_model

>>>>>>> Stashed changes
# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    complete = models.BooleanField(default=False)
    created_date = models.TimeField(auto_now_add=True)
    updated_date = models.TimeField(auto_now=True)

    def __str__(self):
        return self.title
