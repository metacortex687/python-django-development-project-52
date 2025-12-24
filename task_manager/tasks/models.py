from django.db import models
from ..statuses.models import Status
from ..labels.models import Label
from django.conf import settings

class Task(models.Model):
    name = models.CharField(max_length=25, verbose_name='Имя')
    description = models.TextField(max_length=25, verbose_name='Описание')
    status = models.ForeignKey(Status, on_delete=models.RESTRICT, null=True, verbose_name='Статус')
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.RESTRICT, related_name='created_tasks', verbose_name='Автор')
    executor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='assigned_tasks', verbose_name='Исполнитель')
    created_at = models.DateTimeField(auto_now_add=True)

    labels = models.ManyToManyField(Label, through='TaskLabel', blank=True, verbose_name='Метки')


class TaskLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.RESTRICT)

