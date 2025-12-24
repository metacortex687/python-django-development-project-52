from .models import Label
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models.deletion import RestrictedError
from django.shortcuts import redirect


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels.html"


class LabelCreate(LoginRequiredMixin, CreateView):
    model = Label
    template_name = "labels_create.html"
    fields = ("name",)
    success_url = reverse_lazy("labels")

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно создана")
        return super().form_valid(form)


class LabelDelete(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels_delete.html"
    success_url = reverse_lazy("labels")

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except RestrictedError:
            messages.error(
                request, "Невозможно удалить метку, потому что она используется"
            )
            return redirect(self.success_url)

        messages.success(self.request, "Метка успешно удалена")

        return response


class LabelUpdate(LoginRequiredMixin, UpdateView):
    model = Label
    fields = ("name",)
    template_name = "labels_update.html"
    success_url = reverse_lazy("labels")

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно изменена")
        return super().form_valid(form)
