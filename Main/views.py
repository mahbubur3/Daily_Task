from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Task


# view all tasks on homepage
class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'


# create a task
class CreateTask(CreateView):
    model = Task
    fields = '__all__'
    template_name = 'Main/create_task.html'
    success_url = reverse_lazy('task_list')


# view details of a task  
class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'


# edit a task
class EditTask(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'Main/edit_task.html'
    success_url = reverse_lazy('task_list')


# delete a task 
class DeleteTask(DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'Main/delete_confirm.html'
    success_url = reverse_lazy('task_list')