from django.contrib import admin
from .models import AuditUniverse
from import_export.admin import ImportExportModelAdmin

class AuditUniverseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('department', 'company', 'country', 'region', 'city', 'branch', 'division')
    list_display_links = ('department',)
    fieldsets = (
        ('Audit Universe', {
            'fields': (('company', 'country'), ('region', 'city'), ('branch', 'division'), 'department')
        }),
    )

admin.site.register(AuditUniverse, AuditUniverseAdmin)