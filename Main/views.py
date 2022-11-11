from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

from .models import Task
from .forms import EditTaskForm, CreateTaskForm, SigninForm, SignupForm


# view all tasks on homepage
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    # show every user task
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        # search 
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
        context['search_input'] = search_input
        return context


# create a task
class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    form_class = CreateTaskForm
    template_name = 'Main/create_task.html'
    success_url = reverse_lazy('task_list')

    # select user to create a task,
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
    form_class = EditTaskForm
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
    template_name = 'Main/signin.html'
    form_class = SigninForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task_list')


# user signup or registration
class UserSignup(FormView):
    template_name = 'Main/signup.html'
    form_class = SignupForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserSignup, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(UserSignup, self).get(*args, **kwargs)