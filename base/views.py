from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView
# if they are not logged in, we dont want to create or delete etc the tasks
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class customloginview(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')  # when user logins, send to the tasklist


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # restricts the logged in user to see the register page
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class tasklist(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'  # to change the name of the object

    def get_context_data(self, **kwargs):              # for the particular person
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(
            user=self.request.user)       #
        context['count'] = context['tasks'].filter(
            complete=False).count()       # to know the incomplete items
        return context


class taskdetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


# wen we create a task, send the user back to the list
class taskcreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')      # redirecting

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(taskcreate, self).form_valid(form)


class taskupdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class taskdelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    # when we delete an user, it should redirect
    success_url = reverse_lazy('tasks')
    template_name = 'base/task_delete.html'
