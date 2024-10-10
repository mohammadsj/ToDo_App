from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from todo.models import Task
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def common_user():
    return User.objects.create(username="test", password="a/@123456")


@pytest.fixture
def task(common_user):
    return Task.objects.create(user=common_user, title="test", complete=False)


@pytest.mark.django_db
class TestTodoAPI:

    def setup_method(self):
        self.todo_list_url = reverse("todo:api-v1:todo-list")
        self.todo_detail_url = lambda task_id: reverse(
            "todo:api-v1:todo-detail", args=[task_id]
        )

    def test_get_tasks_not_logged_in(self, api_client):
        response = api_client.get(self.todo_list_url)
        assert response.status_code == 401

    def test_get_tasks_logged_in(self, api_client, common_user):
        api_client.force_authenticate(user=common_user)
        response = api_client.get(self.todo_list_url)
        assert response.status_code == 200

    def test_create_task_success(self, api_client, common_user):
        data = {"title": "test", "complete": True}

        api_client.force_authenticate(user=common_user)
        response = api_client.post(self.todo_list_url, data)
        assert response.status_code == 201

    def test_create_task_invalid(self, api_client, common_user):
        data = {"complete": True}

        api_client.force_authenticate(user=common_user)
        response = api_client.post(self.todo_list_url, data)
        assert response.status_code == 400

    def test_task_creation(self, task, common_user):
        assert Task.objects.count() == 1
        assert task.title == "test"
        assert task.user == common_user

    def test_complete_task_response(self, api_client, task, common_user):
        url = self.todo_detail_url(task.id)
        data = {"complete": True}
        api_client.force_authenticate(user=common_user)
        response = api_client.patch(url, data)
        assert response.status_code == 200
        task.refresh_from_db()
        assert task.complete is True

    def test_delete_task(self, api_client, task, common_user):
        url = self.todo_detail_url(task.id)
        api_client.force_authenticate(user=common_user)
        response = api_client.delete(url)
        assert response.status_code == 204
        assert Task.objects.count() == 0

    def test_get_single_task_not_found(self, api_client, common_user):
        url = self.todo_detail_url(999)
        api_client.force_authenticate(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 404

    def test_get_single_task_response(self, api_client, task, common_user):
        url = self.todo_detail_url(task.id)
        api_client.force_authenticate(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 200
