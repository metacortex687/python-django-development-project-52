from .models import Status
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class StatusListView(LoginRequiredMixin,ListView):
    model = Status
    template_name = 'statuses.html'    

class StatusCreate(LoginRequiredMixin,CreateView):
    model = Status
    template_name = 'statuses_create.html' 
    fields = ('name',)
    success_url = reverse_lazy('statuses')   

class StatusDelete(LoginRequiredMixin,DeleteView):
    model = Status
    template_name = 'statuses_delete.html' 
    success_url = reverse_lazy('statuses') 

class StatusUpdate(LoginRequiredMixin,UpdateView):
    model = Status
    fields = ('name',)
    template_name = 'statuses_update.html' 
    success_url = reverse_lazy('statuses')   