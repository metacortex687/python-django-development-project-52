from django.contrib.auth.models import User
from django.views.generic.list import ListView

class UserListView(ListView):
    model = User
    template_name = 'users.html'
