from django.contrib import admin
from .models import RiskOwner, TypeOfRisk, ResponseStrategy, TypeOfControl, ControlFrequency, ControlOwner, StrategicImportanceList, Function, MajorProcess, SubProcess
from import_export.admin import ImportExportModelAdmin

class TypeOfRiskAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('type_of_risk', 'risk_description')

class ResponseStrategyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('response_strategy', 'response_description')

class TypeOfControlAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('type_of_control', 'type_of_control_description')

class ControlFrequencyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('control_frequency', 'control_frequency_description')

class ControlOwnerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('control_owner',)

class RiskOwnerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('risk_owner',)

class StrategicImportanceListAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

class FunctionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

class MajorProcessAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

class SubProcessAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

admin.site.register(RiskOwner, RiskOwnerAdmin)
admin.site.register(TypeOfRisk, TypeOfRiskAdmin)
admin.site.register(ResponseStrategy, ResponseStrategyAdmin)
admin.site.register(TypeOfControl, TypeOfControlAdmin)
admin.site.register(ControlFrequency, ControlFrequencyAdmin)
admin.site.register(ControlOwner, ControlOwnerAdmin)
admin.site.register(StrategicImportanceList, StrategicImportanceListAdmin)
admin.site.register(Function, FunctionAdmin)
admin.site.register(MajorProcess, MajorProcessAdmin)
admin.site.register(SubProcess, SubProcessAdmin)