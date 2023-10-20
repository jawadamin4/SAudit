from django.db import models

class RiskOwner(models.Model):
    risk_owner = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.risk_owner
    
    class Meta:
        verbose_name = "Risk Owner"
        verbose_name_plural = "Risk Owner"
        ordering = ['risk_owner']

class TypeOfRisk(models.Model):
    type_of_risk = models.CharField(max_length=100, unique=True)
    risk_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.type_of_risk

    class Meta:
        verbose_name = "Type of Risk"
        verbose_name_plural = "Type of Risk"
        ordering = ['type_of_risk']

class ResponseStrategy(models.Model):
    response_strategy = models.CharField(max_length=100, unique=True)
    response_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.response_strategy
    
    class Meta:
        verbose_name = "Response Strategy"
        verbose_name_plural = "Response Strategy"
        ordering = ['response_strategy']

class TypeOfControl(models.Model):
    type_of_control = models.CharField(max_length=100, unique=True)
    type_of_control_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.type_of_control
    
    class Meta:
        verbose_name = "Type of Control"
        verbose_name_plural = "Type of Control"
        ordering = ['type_of_control']

class ControlFrequency(models.Model):
    control_frequency = models.CharField(max_length=100, unique=True)
    control_frequency_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.control_frequency
    
    class Meta:
        verbose_name = "Control Frequency"
        verbose_name_plural = "Control Frequency"
        ordering = ['control_frequency']

class ControlOwner(models.Model):
    control_owner = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.control_owner
    
    class Meta:
        verbose_name = "Control Owner"
        verbose_name_plural = "Control Owner"
        ordering = ['control_owner']

class StrategicImportanceList(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Strategic Importance List"
        verbose_name_plural = "Strategic Importance List"
        ordering = ['name']

class Function(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Function"
        verbose_name_plural = "Function"
        ordering = ['name']

class MajorProcess(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Major Process"
        verbose_name_plural = "Major Process"
        ordering = ['name']

class SubProcess(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sub Process"
        verbose_name_plural = "Sub Process"
        ordering = ['name']