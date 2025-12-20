from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.views.generic.list import ListView


class HomePageView(TemplateView):
    template_name = 'index.html'

class UserListView(ListView):
    model = User
    template_name = 'users.html'

