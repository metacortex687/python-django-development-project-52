from django.urls import path
from . import views

urlpatterns = [
    path('users/',views.UserListView.as_view(), name='users'),
    path('login/',views.UserLoginView.as_view(), name='login'),
    path('logout/',views.UserLogoutView.as_view(), name='logout'),
    path('users/create/',views.CreateUserView.as_view(), name='user_create'),
    path('users/<int:pk>/update/',views.UpdateUserView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/',views.DeleteUserView.as_view(), name='user_delete'),

]
