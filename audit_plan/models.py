from django.db import models
import datetime
from audit_plan_setup.models import PublicHoliday, Auditor
from datetime import timedelta

YEAR_CHOICES = [(year, year) for year in range(datetime.date.today().year, datetime.date.today().year + 5)]

class StartAudit(models.Model):
    year = models.IntegerField(choices=YEAR_CHOICES, null=True)
    level = models.CharField(max_length=100, choices=[('company', 'company'), ('country', 'country'), ('region', 'region'), ('city', 'city'), ('branch', 'branch'), ('division', 'division'), ('department', 'department'), ('function', 'function'), ('major_process', 'major_process'), ('sub_process', 'sub_process')], null=True)
    approval_status = models.CharField(max_length=100, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], null=True, blank=True, default='Pending')

    def __str__(self) -> str:
        return f"{self.year} | {self.level}"
    
    class Meta:
        verbose_name = "Audit Year"
        verbose_name_plural = "Audit Year"
        unique_together = ('year', 'level')

class AuditDepartment(models.Model):
    start_audit = models.ForeignKey(StartAudit, on_delete=models.SET_NULL, null=True, blank=False)     
    audit_year = models.IntegerField(null=True, blank=True) 
    level_type = models.CharField(max_length=100, null=True, blank=True) 
    level_name = models.CharField(max_length=100, null=True, blank=True) 
    residual_score = models.CharField(max_length=100, null=True, blank=True) 
    count = models.IntegerField(default=0, null=True, blank=True) 
    risk_assessment = models.CharField(max_length=10, null=True, blank=True)     
    risk_assessment_by_auditor = models.CharField(max_length=100, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], null=True, blank=True)
    strategic_importance_score = models.CharField(max_length=100, null=True, blank=True) 
    count_2 = models.IntegerField(default=0, null=True, blank=True) 
    strategic_importance = models.CharField(max_length=100, null=True, blank=True) 
    strategic_importance_by_auditor = models.CharField(max_length=100, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], null=True, blank=True)
    last_audit = models.CharField(max_length=100, choices=[('Less than 6', 'Less than 6'), ('6 to 12', '6 to 12'), ('12 to 18', '12 to 18'), ('18 to 24', '18 to 24'), ('More than 24', 'More than 24')], null=True, blank=True)
    total_priority_score = models.CharField(max_length=100, null=True, blank=True) 
    start_date = models.DateField(null=True, blank=True, default=datetime.date.today)
    number_of_hours_per_day = models.PositiveIntegerField(null=True, blank=True, default=0)
    total_days = models.PositiveIntegerField(null=True, blank=True, default=0)
    select_for_audit = models.CharField(max_length=100, choices=[('Yes', 'Yes'), ('No', 'No')], null=True, blank=True)
    number_of_auditor = models.IntegerField(default=0, null=True, blank=True)
    name_of_auditor = models.ManyToManyField(Auditor, blank=True)
    total_hours = models.PositiveIntegerField(null=True, blank=True) 
    end_date = models.DateField(null=True, blank=True) 
    start_audit_process = models.CharField(max_length=100, choices=[('Yes', 'Yes'), ('No', 'No')], null=True, blank=True, default='No')

    def calculate_end_date(self):
        end_date = self.start_date
        days_to_add = self.total_days - 1
        while days_to_add > 0:
            end_date += timedelta(days=1)
            if end_date.weekday() in (4, 5):
                continue
            if PublicHoliday.objects.filter(date=end_date).exists():
                continue
            days_to_add -= 1
        return end_date

    def __str__(self) -> str:
        return f" "

    def save(self, *args, **kwargs):
        risk_assessment_values = {'Low': 1, 'Medium': 2, 'High': 3}
        strategic_importance_values = {'Low': 1, 'Medium': 2, 'High': 3}
        last_audit_value = {'Less than 6': 1, '6 to 12': 2, '12 to 18': 3, '18 to 24': 4, 'More than 24': 5}
        risk_assessment_score = risk_assessment_values.get(self.risk_assessment_by_auditor, 0)
        strategic_importance_score = strategic_importance_values.get(self.strategic_importance_by_auditor, 0)
        last_audit_score = last_audit_value.get(self.last_audit, 0)
        total_priority_score = risk_assessment_score + strategic_importance_score + last_audit_score
        if total_priority_score >= 8:
            self.total_priority_score = 'High'
        elif total_priority_score >= 5:
            self.total_priority_score = 'Medium'
        elif total_priority_score == 0:
            self.total_priority_score = 'None'
        else:
            self.total_priority_score = 'Low'
        self.end_date = self.calculate_end_date()
        self.total_hours = self.total_days * self.number_of_hours_per_day * self.number_of_auditor
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Start Audit Planning"
        verbose_name_plural = "Start Audit Planning"