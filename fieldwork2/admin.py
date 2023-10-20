from django.contrib import admin
from .models import AuditInProgress, AuditPorgram

class AuditInProgressAdmin(admin.TabularInline):
    model = AuditPorgram
    extra = 0
    readonly_fields = ('risk_details', 'response_action', 'audit_procedure')
    fields = ('risk_details', 'response_action', 'audit_procedure', 'total_population', 'sample_size', 'test_result', 'information_required', 'move_to_issue_control')

    def has_add_permission(self, request, obj=None):
        return False

class AuditInProgressAdmin2(admin.TabularInline):
    model = AuditPorgram
    extra = 0
    readonly_fields = ('risk_details', 'response_action', 'audit_procedure')
    fields = ('risk_details', 'response_action', 'audit_procedure', 'issue_classification', 'issue_description', 'impact', 'recommendation', 'management_comments')
    filter_horizontal = ('management_comments',)
    verbose_name_plural = 'Issue Control'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        filtered_queryset = queryset.filter(move_to_issue_control='Yes')       
        return filtered_queryset
    
    def has_add_permission(self, request, obj=None):
        return False

class AuditInProgressAdmin3(admin.ModelAdmin):
    list_display = ('level_type', 'level_name', 'start_date', 'actual_start_date',)
    readonly_fields = ('level_type', 'level_name', 'start_date', 'actual_start_date')
    list_editable = ('actual_start_date',)
    fields = ('risk', 'audit_procedure', 'move_to_audit_program')
    inlines = [AuditInProgressAdmin, AuditInProgressAdmin2]
    verbose_name = 'Custom Audit'
    verbose_name_plural = 'Custom Audits'

    def has_add_permission(self, request, obj=None):
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

admin.site.register(AuditInProgress, AuditInProgressAdmin3)