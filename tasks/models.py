from django.db import models
from statuses.models import Status
from django.contrib.auth.models import User

class Task(models.Model):
    name = models.CharField(max_length=25)
    describe = models.TextField(max_length=25)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='created_tasks')
    executor = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='assigned_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

