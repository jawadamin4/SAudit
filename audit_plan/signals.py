from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import models
from .models import StartAudit, AuditDepartment
from risk_assessment.models import RiskAssessment, StrategicImportance
from fieldwork2.models import AuditInProgress

def get_risk_assessment(total_residual_score, count):
    if total_residual_score is None:
        return 'No Data'
    else:
        risk_assessment_value = total_residual_score / count
        if risk_assessment_value <= -1:
            return 'Low'
        elif risk_assessment_value == 0:
            return 'Medium'
        else:
            return 'High'

def get_strategic_importance(strategic_importance_score, count_2):
    if strategic_importance_score is None:
        return 'No Data'
    else:
        strategic_importance_value = strategic_importance_score / count_2
        if strategic_importance_value >= 2.5:
            return 'High'
        elif strategic_importance_value >= 1.5:
            return 'Medium'
        else:
            return 'Low'


@receiver(pre_save, sender=StartAudit)
def update_or_create_audit_departments(sender, instance, **kwargs):
    # Get the original instance from the database
    original_instance = StartAudit.objects.filter(pk=instance.pk).first()

    # Check if it's a new instance or the 'level' has changed
    if not original_instance or original_instance.level != instance.level:
        # If the 'level' has changed or it's a new instance, delete existing AuditDepartments
        AuditDepartment.objects.filter(start_audit=instance).delete()
        level_type = instance.level
        audit_year = instance.year
        departments = []
        if level_type == 'company':
            departments = RiskAssessment.objects.values_list('company', flat=True).distinct()
        elif level_type == 'country':
            departments = RiskAssessment.objects.values_list('country', flat=True).distinct()
        elif level_type == 'region':
            departments = RiskAssessment.objects.values_list('region', flat=True).distinct()
        elif level_type == 'city':
            departments = RiskAssessment.objects.values_list('city', flat=True).distinct()
        elif level_type == 'branch':
            departments = RiskAssessment.objects.values_list('branch', flat=True).distinct()
        elif level_type == 'division':
            departments = RiskAssessment.objects.values_list('division', flat=True).distinct()
        elif level_type == 'department':
            departments = RiskAssessment.objects.values_list('department', flat=True).distinct()
        elif level_type == 'function':
            departments = RiskAssessment.objects.values_list('function', flat=True).distinct()
        elif level_type == 'major_process':
            departments = RiskAssessment.objects.values_list('major_process', flat=True).distinct()
        elif level_type == 'sub_process':
            departments = RiskAssessment.objects.values_list('sub_process', flat=True).distinct()

        for department in departments:
            total_residual_score = \
                RiskAssessment.objects.filter(**{level_type: department}).aggregate(models.Sum('residual_score'))[
                    'residual_score__sum']
            count = RiskAssessment.objects.filter(**{level_type: department}).count()
            risk_assessment = get_risk_assessment(total_residual_score, count)
            strategic_importance_score = StrategicImportance.objects.filter(**{level_type: department}).aggregate(
                models.Sum('strategic_importance_score'))['strategic_importance_score__sum']
            count_2 = StrategicImportance.objects.filter(**{level_type: department}).count()
            strategic_importance = get_risk_assessment(strategic_importance_score, count_2)

            # Create new entries with the correct level name
            AuditDepartment.objects.create(
                start_audit=instance,
                level_type=level_type,
                level_name=department,
                audit_year=audit_year,
                residual_score=total_residual_score or 0,
                count=count,
                risk_assessment=risk_assessment,
                strategic_importance_score=strategic_importance_score or 0,
                count_2=count_2,
                strategic_importance=strategic_importance
            )

@receiver(post_save, sender=AuditDepartment)
def create_or_update_rcm(sender, instance, created, **kwargs):
    level_type = instance.level_type
    level_name = instance.level_name
    start_date = instance.start_date
    start_audit_process = instance.start_audit_process
    if start_audit_process == 'Yes':
        try:
            test_model = AuditInProgress.objects.get(level_type=level_type, level_name=level_name, start_date=start_date,)
            test_model.save()
        except AuditInProgress.DoesNotExist:
            AuditInProgress.objects.create(level_type=level_type, level_name=level_name, start_date=start_date,)