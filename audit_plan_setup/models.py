from django.db import models
from django.contrib.auth.models import User

class Auditor(models.Model):
    name = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False, unique=True)
    profile_picture = models.ImageField(upload_to='auditor_profiles/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    def __str__(self):
        return self.name.username

    class Meta:
        verbose_name = "Auditor"
        verbose_name_plural = "Auditor"

class Auditee(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False, unique=True)
    profile_picture = models.ImageField(upload_to='auditee_profiles/', null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Auditee"
        verbose_name_plural = "Auditees"

class PublicHoliday(models.Model):
    date = models.DateField(null=True, blank=True, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Public Holiday"
        verbose_name_plural = "Public Holiday"