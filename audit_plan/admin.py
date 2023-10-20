from django.contrib import admin
from .models import StartAudit, AuditDepartment

class AuditDepartmentAdmin(admin.TabularInline):
    model = AuditDepartment
    extra = 0
    fields = ('level_name', 'risk_assessment', 'risk_assessment_by_auditor', 'strategic_importance', 'strategic_importance_by_auditor', 'last_audit')
    readonly_fields = ('risk_assessment', 'strategic_importance', 'level_name')
    verbose_name_plural = 'Key Planning Factors'

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False

class AuditDepartmentAdmin2(admin.TabularInline):
    model = AuditDepartment
    extra = 0
    fields = ('level_name', 'total_priority_score', 'select_for_audit', 'start_date', 'number_of_hours_per_day', 'total_days', 'number_of_auditor', 'name_of_auditor', 'total_hours', 'end_date', 'start_audit_process')
    readonly_fields = ('level_name', 'total_priority_score', 'total_hours', 'end_date')
    verbose_name_plural = 'Annual Planning & Resource Planning'

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False

class StartAuditAdmin(admin.ModelAdmin):
    list_display = ('year','level', 'approval_status')
    inlines = [AuditDepartmentAdmin, AuditDepartmentAdmin2]

    def has_add_permission(self, request):
        pending_records = StartAudit.objects.filter(approval_status='Pending').exists()
        if pending_records:
            return False
        else:
            return True
    
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': ' . '}
        return super().changelist_view(request, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = {'title': ''}
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = {'title': ''}
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

admin.site.register(StartAudit, StartAuditAdmin)
