from django.db import models

class InformationRequired(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    attachments = models.FileField(upload_to='attachments/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Information Required"
        verbose_name_plural = "Information Required"

class ManagementComments(models.Model):
    comment_by = models.CharField(max_length=100, choices=[('Management', 'Management'), ('Auditor', 'Auditor')], null=True, blank=True)
    comments = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.comments

    class Meta:
        verbose_name = "Management Comments"
        verbose_name_plural = "Management Comments"