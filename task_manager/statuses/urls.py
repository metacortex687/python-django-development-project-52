from django.urls import path
from . import views

urlpatterns = [
    path("", views.StatusListView.as_view(), name="statuses"),
    path("create/", views.StatusCreate.as_view(), name="statuses_create"),
    path(
        "<int:pk>/delete/", views.StatusDelete.as_view(), name="statuses_delete"
    ),
    path(
        "<int:pk>/update/", views.StatusUpdate.as_view(), name="statuses_update"
    ),
]
