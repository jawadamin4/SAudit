from django.db import models

class AuditUniverse(models.Model):
    company = models.CharField(max_length=100, null=True, blank=True,)
    country = models.CharField(max_length=100, null=True, blank=True,)
    region = models.CharField(max_length=100, null=True, blank=True,)
    city = models.CharField(max_length=100, null=True, blank=True,)
    branch = models.CharField(max_length=100, null=True, blank=True,)
    division = models.CharField(max_length=100, null=True, blank=True,)
    department = models.CharField(max_length=100, null=True, blank=False)

    def __str__(self):
        return f'{self.company} | {self.country} | {self.city} | {self.department}'
    
    def save(self, *args, **kwargs):
        fields_to_check = ['company', 'country', 'region', 'city', 'branch', 'division']
        for field_name in fields_to_check:
            field_value = getattr(self, field_name)
            if field_value is None or field_value.strip() == '':
                setattr(self, field_name, '-')
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Audit Universe"
        verbose_name_plural = "Audit Universe"
        unique_together = ('company', 'country', 'region', 'city', 'branch', 'division', 'department')