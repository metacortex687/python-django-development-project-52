from .models import Status
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

class StatusListView(LoginRequiredMixin,ListView):
    model = Status
    template_name = 'statuses.html'    

class StatusCreate(LoginRequiredMixin,CreateView):
    model = Status
    template_name = 'statuses_create.html' 
    fields = ('name',)
    success_url = reverse_lazy('statuses') 

    def form_valid(self, form):
        messages.success(self.request,'Статус успешно создан')
        return super().form_valid(form)
      

class StatusDelete(LoginRequiredMixin,DeleteView):
    model = Status
    template_name = 'statuses_delete.html' 
    success_url = reverse_lazy('statuses') 

    def form_valid(self, form):
        messages.success(self.request,'Статус успешно удален')
        return super().form_valid(form)

class StatusUpdate(LoginRequiredMixin,UpdateView):
    model = Status
    fields = ('name',)
    template_name = 'statuses_update.html' 
    success_url = reverse_lazy('statuses')   

    def form_valid(self, form):
        messages.success(self.request,'Статус успешно изменен')
        return super().form_valid(form)