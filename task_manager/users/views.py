from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=False, label='Имя')
    last_name = forms.CharField(required=False, label='Фамилия')

    class Meta(UserCreationForm.Meta):
        fields=('username','first_name','last_name','password1','password2')  


class CustomUserChangeFormForm(UserChangeForm):
    password = None
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль', help_text='<ul><li>Ваш пароль должен содержать как минимум 3 символа.</li></ul>')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля', help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.')   

    class Meta(UserChangeForm.Meta):
        fields=('username','first_name','last_name',)

    def clean_password1(self):
        p1 = self.cleaned_data.get('password1')
        if len(p1) < 3:
            raise forms.ValidationError('Ваш пароль должен содержать как минимум 3 символа.')
        return p1
    
    def clean(self):
        cleaned = super().clean()

        if cleaned.get('password1') != cleaned.get('password2'):
            self.add_error('password2','Пароли не совпадают') 

        return cleaned  
    
    def save(self, commit = ...):
        self.instance.set_password(self.cleaned_data['password1'])
        return super().save(commit)
    
    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)
    
    

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
    
    def form_valid(self, form):
        messages.success(self.request,'Пользователь успешно зарегистрирован')
        return super().form_valid(form)


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeFormForm
    template_name = 'user_update.html'
    success_url = reverse_lazy('users')

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            messages.error(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)
    

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'user_delete.html'
    success_url = reverse_lazy('users')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            messages.error(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().handle_no_permission()