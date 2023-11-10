from django.db import models

class Informationrequest(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Information Request"
        verbose_name_plural = "Information Requests"



class ManagementComments(models.Model):
    comment_by = models.CharField(max_length=100, choices=[('Management', 'Management'), ('Auditor', 'Auditor')], null=True, blank=True)
    comments = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.comments

    class Meta:
        verbose_name = "Management Comments"
        verbose_name_plural = "Management Comments"