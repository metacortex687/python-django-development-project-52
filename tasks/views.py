from .models import Task
from labels.models import Label

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'tasks.html'    

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    template_name = 'tasks_create.html' 
    fields = ('name','describe','status','executor')
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        
        return super().form_valid(form)
       

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    template_name = 'tasks_delete.html' 
    success_url = reverse_lazy('tasks') 


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ('name','describe','status','executor', 'labels')
    template_name = 'tasks_update.html' 

    def get_success_url(self):
        return reverse_lazy('tasks_detail', args=[self.object.pk])
    

class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    fields = ('name','describe','status','executor')
    template_name = 'tasks_detail.html' 
    success_url = reverse_lazy('tasks')   

