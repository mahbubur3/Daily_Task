from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task


# view all tasks on homepage
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    # show every user task
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context


# create a task
class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    template_name = 'Main/create_task.html'
    success_url = reverse_lazy('task_list')

    # select user to create a task
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


# view details of a task  
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'


# edit a task
class EditTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'Main/edit_task.html'
    success_url = reverse_lazy('task_list')


# delete a task 
class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'Main/delete_confirm.html'
    success_url = reverse_lazy('task_list')


# user signin
class UserSignin(LoginView):
    fields = '__all__'
    template_name = 'Main/signin.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task_list')
