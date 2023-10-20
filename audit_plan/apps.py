from django.apps import AppConfig

class AuditPlanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'audit_plan'
    verbose_name = '4-Audit Plan'

    def ready(self):
        import audit_plan.signals