from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy

class UserListView(ListView):
    model = User
    template_name = 'users.html'    


class CreateUserView(CreateView):
    template_name = 'user_create.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')    
