from django.urls import path , include
from . import views
app_name = 'todo'

urlpatterns = [
    path('',views.TaskListView.as_view(),name='TaskListView'),
    path('created/',views.TaskCreate.as_view(),name='TaskCreate'),
    path('complete/<int:pk>',views.TaskComplete.as_view(),name='TaskComplete'),
    path('returncomplete/<int:pk>',views.ReturnTaskComplete.as_view(),name='ReturnTaskComplete'),
    path('Update/<int:pk>',views.TaskUpdate.as_view(),name='TaskUpdate'),
    path('Delete/<int:pk>',views.TaskDelete.as_view(),name='TaskDelete'),
    path('api/v1/',include('todo.api.v1.urls'),name='todo-api-v1'),
]
