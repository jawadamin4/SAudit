from django.db import models
from risk_assessment.models import RiskAssessment
from fieldwork_setup.models import InformationRequired, ManagementComments

class AuditInProgress(models.Model):
    level_type = models.CharField(max_length=100, null=True, blank=True)
    level_name = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.CharField(max_length=100, null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    start_audit_process = models.CharField(max_length=100, null=True, blank=True)
    risk = models.ForeignKey(RiskAssessment, on_delete=models.SET_NULL, null=True, blank=True)
    audit_procedure = models.CharField(max_length=100, null=True, blank=True)
    move_to_audit_program = models.CharField(max_length=100, choices=[('Yes', 'Yes'), ('No', 'No')], null=True, blank=True)
    risk_details = models.CharField(max_length=100, null=True, blank=True)
    response_action = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            self.risk_details = self.risk.risk_details
            self.response_action = self.risk.response_action
        except:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.level_name
    
    class Meta:
        verbose_name = "Risk Control Matrix (RCM)"
        verbose_name_plural = "Audit In Progress"
        ordering = ['risk']

class AuditPorgram(models.Model):
    audit_in_progress = models.ForeignKey(AuditInProgress, on_delete=models.SET_NULL, null=True, blank=False)
    risk_details = models.CharField(max_length=100, null=True, blank=True)
    response_action = models.CharField(max_length=100, null=True, blank=True)
    audit_procedure = models.CharField(max_length=100, null=True, blank=True)
    total_population = models.PositiveIntegerField(null=True, blank=True, default=0)
    sample_size = models.PositiveIntegerField(null=True, blank=True, default=0)
    information_required = models.ManyToManyField(InformationRequired, blank=True)
    test_result = models.CharField(max_length=100, null=True, blank=True)
    move_to_issue_control = models.CharField(max_length=100, choices=[('Yes', 'Yes'), ('No', 'No')], null=True, blank=True)
    issue_classification = models.CharField(max_length=100, choices=[('Option 1', 'Option 1'), ('Option 2', 'Option 2')], null=True, blank=True)
    issue_description = models.CharField(max_length=100, null=True, blank=True)
    impact = models.CharField(max_length=100, null=True, blank=True)
    recommendation = models.CharField(max_length=100, null=True, blank=True)
    management_comments = models.ManyToManyField(ManagementComments, blank=True)
    
    class Meta:
        verbose_name = "Audit Program"
        verbose_name_plural = "Audit Program"

    def __str__(self) -> str:
        return f" "