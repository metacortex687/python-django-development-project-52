from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django import forms

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        fields=('username','first_name','last_name','password1','password2')  

    # def save(self, commit = ...):
    #     user = 
    #     return super().save(commit)
    




class UserLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request,'Вы залогинены')
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request,'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)    

class UserListView(ListView):
    model = User
    template_name = 'users.html'    


class CreateUserView(CreateView):
    template_name = 'user_create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login') 
    


class UpdateUserView(UpdateView):
    model = User
    template_name = 'user_update.html'
    success_url = reverse_lazy('users')
    fields = ('username', 'first_name', 'last_name')


class DeleteUserView(DeleteView):
    model = User
    template_name = 'user_delete.html'
    success_url = reverse_lazy('users')