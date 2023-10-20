from django.db import models
from django.contrib.auth.models import User

class Auditor(models.Model):
    name = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False, unique=True)

    def __str__(self):
        return self.name.username

    class Meta:
        verbose_name = "Auditor"
        verbose_name_plural = "Auditor"

class PublicHoliday(models.Model):
    date = models.DateField(null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Public Holiday"
        verbose_name_plural = "Public Holiday"