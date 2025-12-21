from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('users/',views.UserListView.as_view(),name='users'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
