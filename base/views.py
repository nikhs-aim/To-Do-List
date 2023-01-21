from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin      # if they are not logged in, we dont want to create or delete etc the tasks
from .models import task
from django.urls import reverse_lazy


# Create your views here.

class customloginview(LoginView):
    template_name='base/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('tasks')     #when user logins, send to the tasklist




class tasklist(LoginRequiredMixin,ListView):
    model=task
    context_object_name='tasks'  #to change the name of the object
    
    def get_context_data(self, **kwargs):              # for the particular person
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)       # 
        context['count']=context['tasks'].filter(complete=False).count()       # to know the incomplete items
        return context


class taskdetail(LoginRequiredMixin,DetailView):
    model=task
    context_object_name='task'
    
class taskcreate(LoginRequiredMixin,CreateView):      # wen we create a task, send the user back to the list
    model=task
    fields="__all__"
    success_url=reverse_lazy('tasks')      # redirecting

class taskupdate(LoginRequiredMixin,UpdateView):
    model=task
    fields="__all__"
    success_url=reverse_lazy('tasks') 

class taskdelete(LoginRequiredMixin,DeleteView):
    model=task
    context_object_name='task'
    success_url=reverse_lazy('tasks')     #when we delete an user, it should redirect
    template_name='base/task_delete.html'