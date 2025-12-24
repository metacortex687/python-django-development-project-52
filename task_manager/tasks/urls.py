from django.urls import path
from . import views

urlpatterns = [
    path('',views.TaskListView.as_view(),name='tasks'),
    path('create/',views.TaskCreate.as_view(),name='tasks_create'),
    path('<int:pk>/delete/',views.TaskDelete.as_view(), name='tasks_delete'),
    path('<int:pk>/update/',views.TaskUpdate.as_view(), name='tasks_update'),
    path('<int:pk>/',views.TaskDetailView.as_view(), name='tasks_detail'),
]
