from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True , blank=True)
    title = models.CharField(max_length=255)
    complete = models.BooleanField(default=False)
    
    created_date = models.TimeField(auto_now_add=True)
    updated_date = models.TimeField(auto_now=True)
    def __str__(self):
        return self.title
    