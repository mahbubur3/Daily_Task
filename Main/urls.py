from django.urls import path

from .views import TaskList, CreateTask, TaskDetail, EditTask, DeleteTask


urlpatterns = [
    path('', TaskList.as_view(), name='task_list'),
    path('create/', CreateTask.as_view(), name='create'),
    path('task/<str:pk>/', TaskDetail.as_view(), name='detail'),
    path('edit/<str:pk>/', EditTask.as_view(), name='edit'),
    path('delete/<str:pk>/', DeleteTask.as_view(), name='delete'),
]
