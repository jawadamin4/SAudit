from django.contrib import admin
from .models import RiskAssessment, StrategicImportance
from import_export.admin import ImportExportModelAdmin


# from column_toggle.admin import ColumnToggleModelAdmin

class RiskAssessmentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('overall_inherent_risk_rating', 'overall_control_rating', 'residual_risk_rating')
    exclude = ('risk_score', 'control_score', 'residual_score')
    list_display = (
    'department', 'company', 'country', 'region', 'city', 'branch', 'division', 'function', 'major_process',
    'sub_process', 'risk_details', 'risk_owner', 'type_of_risk', 'impact', 'likelihood', 'overall_inherent_risk_rating',
    'response_strategy', 'response_action', 'type_of_control', 'control_frequency', 'control_owner', 'control_design',
    'effectiveness', 'overall_control_rating', 'residual_risk_rating')
    list_display_links = ('department',)
    search_fields = (
    'department', 'company', 'country', 'region', 'city', 'branch', 'division', 'function', 'major_process',
    'sub_process', 'risk_details', 'risk_owner', 'type_of_risk', 'impact', 'likelihood', 'overall_inherent_risk_rating',
    'response_strategy', 'response_action', 'type_of_control', 'control_frequency', 'control_owner', 'control_design',
    'effectiveness', 'overall_control_rating', 'residual_risk_rating')
    list_per_page = 5
    fieldsets = (
        ('Risk Assessment', {
            'fields': (
            'audit_universe', 'function', 'major_process', 'sub_process', 'risk_details', 'risk_owner', 'type_of_risk',
            'impact', 'likelihood', 'overall_inherent_risk_rating'),
        }),

        ('Response and Control', {
            'fields': (
            'response_action', ('response_strategy', 'type_of_control'), ('control_frequency', 'control_owner'),
            'control_design', 'effectiveness', 'overall_control_rating', 'residual_risk_rating'),
        }),
    )


class StrategicImportanceAdmin(admin.ModelAdmin):
    list_display = ('department', 'division', 'strategic_importance', 'strategic_objective')
    fieldsets = (
        ('Strategic Importance', {
            'fields': ('audit_universe', 'strategic_importance', 'strategic_objective',
                       'strategic_importance_in_next_1_to_5_years'),
        }),
    )


admin.site.register(RiskAssessment, RiskAssessmentAdmin)
admin.site.register(StrategicImportance, StrategicImportanceAdmin)
