from ...models import Task
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated 
from .serializers import TaskSerializer


class ToDoModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()