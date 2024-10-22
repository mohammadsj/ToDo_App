from django.contrib import admin
from .models import Task

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "title",
        "complete",
        "created_date",
    ]
    list_filter = [
        "user",
        "complete",
    ]


admin.site.register(Task, TaskAdmin)
