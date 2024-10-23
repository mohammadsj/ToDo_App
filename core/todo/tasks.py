from celery import shared_task
from .models import Task


@shared_task
def complete_task():
    Task.objects.filter(complete=True).delete()
    return print("task deleted")
