from django.urls import path
from . import views

urlpatterns = [
    path('',views.StatusListView.as_view(),name='statuses'),
    path('create/',views.StatusCreate.as_view(),name='statuses_create'),
    path('<int:pk>/delete/',views.StatusDelete.as_view(), name='statuses_delete'),
    path('<int:pk>/update/',views.StatusUpdate.as_view(), name='statuses_update'),
    # path('',views.StatusListView.as_view(),name='statuses'),

    # path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    # path('users/create/',views.CreateUserView.as_view(), name='user_create'),
    # path('users/<int:pk>/update/',views.UpdateUserView.as_view(), name='user_update'),
    #

]
