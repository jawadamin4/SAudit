from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import render
from .models import AuditInProgress, AuditPorgram, InformationRequired, ChatMessage
from .signals import send_auditor_comment_notification


class InformationRequiredInline(admin.TabularInline):
    model = InformationRequired
    extra = 0
    readonly_fields = ('chat_room_link', 'audit_program', 'name', 'attachments', 'comments')
    exclude = ('Chat_room',)

    def chat_room_link(self, obj):
        if obj.Chat_room:
            url = reverse('room', kwargs={'room_name': obj.Chat_room})
            return format_html(
                f'<div style="display: inline-block; padding: 5px; background-color: #104f18;">'
                f'<a style="color: white; text-decoration: none;" href="{url}">'
                f'<i class="fas fa-comments"> Chat Room'
                f'</a>'
                f'</div>'
            )
        return "Chat Room not available"

    chat_room_link.short_description = 'Chat Room Link'


class AuditInProgressAdmin(admin.TabularInline):
    model = AuditPorgram
    extra = 0
    readonly_fields = ('risk_details', 'response_action', 'audit_procedure')
    fields = (
        'risk_details', 'response_action', 'audit_procedure', 'total_population', 'sample_size', 'information_required',
        'auditee_email', 'create_chatroom', 'test_result', 'move_to_issue_control')

    def has_add_permission(self, request, obj=None):
        return False


class AuditInProgressAdmin2(admin.TabularInline):
    model = AuditPorgram
    extra = 0
    readonly_fields = ('risk_details', 'response_action', 'audit_procedure')
    fields = (
        'risk_details', 'response_action', 'audit_procedure', 'issue_classification', 'issue_description', 'impact',
        'recommendation', 'management_comments')
    filter_horizontal = ('management_comments',)
    verbose_name_plural = 'Issue Control'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        filtered_queryset = queryset.filter(move_to_issue_control='Yes')
        return filtered_queryset

    def has_add_permission(self, request, obj=None):
        return False


class AuditInProgressAdmin3(admin.ModelAdmin):
    list_display = ('level_type', 'level_name', 'start_date', 'actual_start_date')
    readonly_fields = ('level_type', 'level_name', 'start_date', 'actual_start_date')
    list_editable = ('actual_start_date',)
    fields = ('risk', 'audit_procedure', 'move_to_audit_program')
    inlines = [AuditInProgressAdmin, InformationRequiredInline, AuditInProgressAdmin2]
    verbose_name = 'Custom Audit'
    verbose_name_plural = 'Custom Audits'

    def has_add_permission(self, request, obj=None):
        return False

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
admin.site.register(InformationRequired)
admin.site.register(ChatMessage)
