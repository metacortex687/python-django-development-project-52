from .models import Task
from ..labels.models import Label

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

from django_filters.views import FilterView 
from .filters import TaskFilter 
from django.contrib import messages
from django.shortcuts import redirect


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks.html'
    filterset_class = TaskFilter  


class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    template_name = 'tasks_create.html' 
    fields = ('name','describe','status','executor')
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user

        messages.success(self.request,'Задача успешно создана')

        return super().form_valid(form)
       

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    template_name = 'tasks_delete.html' 
    success_url = reverse_lazy('tasks') 

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            messages.error(self.request,'Задачу может удалить только ее автор')
            return redirect('tasks')

        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):

        messages.success(self.request,'Задача успешно удалена')

        return super().form_valid(form)   


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ('name','describe','status','executor', 'labels')
    template_name = 'tasks_update.html' 

    def get_success_url(self):
        return reverse_lazy('tasks_detail', args=[self.object.pk])
    
    def form_valid(self, form):
        messages.success(self.request,'Задача успешно изменена')
        return super().form_valid(form)  
     

class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    fields = ('name','describe','status','executor')
    template_name = 'tasks_detail.html' 
    success_url = reverse_lazy('tasks')   

