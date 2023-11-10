from .models import AuditInProgress, AuditPorgram, InformationRequired
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=AuditInProgress)
def create_audit_departments(sender, instance, created, **kwargs):
    move_to_audit_program = instance.move_to_audit_program
    risk_details = instance.risk_details
    response_action = instance.response_action
    audit_procedure = instance.audit_procedure
    if move_to_audit_program == 'Yes':
        try:
            test_model = AuditPorgram.objects.get(audit_in_progress=instance, risk_details=risk_details,
                                                  response_action=response_action, audit_procedure=audit_procedure, )
            test_model.save()
        except AuditPorgram.DoesNotExist:
            AuditPorgram.objects.create(audit_in_progress=instance, risk_details=risk_details,
                                        response_action=response_action, audit_procedure=audit_procedure, )


@receiver(post_save, sender=AuditPorgram)
def send_information_required_email(sender, instance, created, **kwargs):
    # Send an email to the auditee
    instance.send_information_required_email()


def send_auditor_comment_notification(information_required):
    subject = 'Auditor Comment on Uploaded Information'
    message = f'Dear Auditee,\n\nAn auditor has added the following comment to the uploaded information:\n\n{information_required.auditor_comments}\n\nPlease review the comment and take any necessary action.\n\nThank you for your cooperation.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [information_required.audit_program.auditee_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


# @receiver(pre_save, sender=InformationRequired)
# def handle_auditor_comments(sender, instance, **kwargs):
#     # Check if the auditor_comments field is about to change
#     if instance.pk:
#         old_instance = InformationRequired.objects.get(pk=instance.pk)
#         if old_instance.auditor_comments != instance.auditor_comments:
#             send_auditor_comment_notification(instance)  # Call the notification function
#
#
# # Ensure that the signal handler is connected
# post_save.connect(handle_auditor_comments, sender=InformationRequired)
