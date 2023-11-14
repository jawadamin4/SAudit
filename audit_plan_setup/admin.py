from django.contrib import admin
from .models import Auditor, PublicHoliday,Auditee

admin.site.register(Auditor)
admin.site.register(Auditee)
admin.site.register(PublicHoliday)