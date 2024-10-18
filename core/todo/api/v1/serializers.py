from rest_framework import serializers
from todo.models import Task
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id", "user", "title", "complete")
        read_only_fields = ["user"]

    def create(self, validated_data):
        validated_data["user"] = User.objects.get(
            id=self.context.get("request").user.id
        )
        return super().create(validated_data)
