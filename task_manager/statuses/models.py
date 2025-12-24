from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=25, verbose_name="Имя")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
