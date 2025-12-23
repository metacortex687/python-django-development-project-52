from .models import Label
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class LabelListView(LoginRequiredMixin,ListView):
    model = Label
    template_name = 'labels.html'    

class LabelCreate(LoginRequiredMixin,CreateView):
    model = Label
    template_name = 'labels_create.html' 
    fields = ('name',)
    success_url = reverse_lazy('labels')   

class LabelDelete(LoginRequiredMixin,DeleteView):
    model = Label
    template_name = 'labels_delete.html' 
    success_url = reverse_lazy('labels') 

class LabelUpdate(LoginRequiredMixin,UpdateView):
    model = Label
    fields = ('name',)
    template_name = 'labels_update.html' 
    success_url = reverse_lazy('labels')   