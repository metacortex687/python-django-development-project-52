import django_filters
from .models import Task
from labels.models import Label
from django import forms


class TaskFilter(django_filters.FilterSet):
    self_tasks = django_filters.BooleanFilter(label='Только свои задачи', widget = forms.CheckboxInput(), method='filter_self_tasks')
    label = django_filters.ModelChoiceFilter(label='Метка', queryset=Label.objects.all(), method='filter_label')
    class Meta:
        model = Task
        fields = ['status','executor','label','self_tasks']

    def filter_self_tasks(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(author=self.request.user)
    
    def filter_label(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(labels=value)