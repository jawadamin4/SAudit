from .models import AuditInProgress, AuditPorgram
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=AuditInProgress)
def create_audit_departments(sender, instance, created, **kwargs):
    move_to_audit_program = instance.move_to_audit_program
    risk_details = instance.risk_details
    response_action = instance.response_action
    audit_procedure = instance.audit_procedure
    if move_to_audit_program == 'Yes':
        try:
            test_model = AuditPorgram.objects.get(audit_in_progress=instance, risk_details=risk_details, response_action=response_action, audit_procedure=audit_procedure, )
            test_model.save()
        except AuditPorgram.DoesNotExist:
            AuditPorgram.objects.create(audit_in_progress=instance, risk_details=risk_details, response_action=response_action, audit_procedure=audit_procedure,)