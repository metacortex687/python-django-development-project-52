from django.urls import path
from . import views

urlpatterns = [
    path("", views.LabelListView.as_view(), name="labels"),
    path("create/", views.LabelCreate.as_view(), name="labels_create"),
    path("<int:pk>/delete/", views.LabelDelete.as_view(), name="labels_delete"),
    path("<int:pk>/update/", views.LabelUpdate.as_view(), name="labels_update"),
]
