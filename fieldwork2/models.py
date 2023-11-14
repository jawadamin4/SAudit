from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from audit_plan_setup.models import Auditor
from django.template.loader import render_to_string
from risk_assessment.models import RiskAssessment
from fieldwork_setup.models import ManagementComments, Informationrequest
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings


class InformationRequired(models.Model):
    audit_program = models.ForeignKey("AuditInProgress", on_delete=models.CASCADE, related_name="requirements")
    name = models.CharField(max_length=100, null=True, blank=True)
    attachments = models.FileField(upload_to="information_required/", null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    Chat_room = models.CharField(max_length=100)

    def __str__(self):
        return self.audit_program.level_name

    class Meta:
        verbose_name = "Information Required"
        verbose_name_plural = "Information Required"


class AuditInProgress(models.Model):
    level_type = models.CharField(max_length=100, null=True, blank=True)
    level_name = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.CharField(max_length=100, null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    start_audit_process = models.CharField(max_length=100, null=True, blank=True)
    risk = models.ForeignKey(RiskAssessment, on_delete=models.SET_NULL, null=True, blank=True)
    audit_procedure = models.CharField(max_length=100, null=True, blank=True)
    move_to_audit_program = models.CharField(max_length=100, choices=[('Yes', 'Yes'), ('No', 'No')], null=True,
                                             blank=True)
    risk_details = models.CharField(max_length=100, null=True, blank=True)
    response_action = models.CharField(max_length=100, null=True, blank=True)

    def get_risk_assessment_data(self):
        if self.risk:
            return f"Risk Details: {self.risk.risk_details}, Response Action: {self.risk.response_action}"
        return "No Risk Assessment data available"

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
    auditee_email = models.EmailField(max_length=254)
    information_required = models.ManyToManyField(Informationrequest, blank=True)
    create_chatroom = models.CharField(max_length=10, null=True, blank=True)
    test_result = models.CharField(max_length=100, null=True, blank=True)
    move_to_issue_control = models.CharField(max_length=100, choices=[('Yes', 'Yes'), ('No', 'No')], null=True,
                                             blank=True)
    issue_classification = models.CharField(max_length=100,
                                            choices=[('Option 1', 'Option 1'), ('Option 2', 'Option 2')], null=True,
                                            blank=True)
    issue_description = models.CharField(max_length=100, null=True, blank=True)
    impact = models.CharField(max_length=100, null=True, blank=True)
    uploaded_requirements = models.ManyToManyField(InformationRequired, blank=True)
    recommendation = models.CharField(max_length=100, null=True, blank=True)
    management_comments = models.ManyToManyField(ManagementComments, blank=True)

    def send_information_required_email(self):
        subject = f'Information Required for Audit Program: {self.audit_in_progress.id}'
        requirements = self.information_required.all()
        upload_url = reverse('upload_requirements', args=[self.audit_in_progress.id])

        context = {
            'requirements': requirements,
            'upload_url': upload_url,
            'create_chatroom': self.create_chatroom,
        }

        message = render_to_string('fieldwork2/information_required_email.html', context)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.auditee_email]

        email = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        email.content_subtype = "html"  # Set content type to HTML
        email.send()

    class Meta:
        verbose_name = "Audit Program"
        verbose_name_plural = "Audit Program"

    def __str__(self) -> str:
        return f" "


class ChatMessage(models.Model):
    room_name = models.CharField(max_length=100)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
