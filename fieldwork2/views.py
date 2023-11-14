from django.shortcuts import render, redirect
from fieldwork2.models import AuditPorgram, InformationRequired, AuditInProgress
from .forms import UploadRequirementsForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required()
def upload_requirements(request, audit_program_id):
    auditinProgress = AuditInProgress.objects.get(id=audit_program_id)
    print(auditinProgress.level_name)
    audit_program = AuditPorgram.objects.get(audit_in_progress=auditinProgress.id)
    print(audit_program.audit_in_progress.level_name)
    requirement_list = audit_program.information_required.all()
    chat_room = audit_program.create_chatroom
    if request.method == 'POST':
        form = UploadRequirementsForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_files = request.FILES.getlist('information_required')
            name = form.cleaned_data.get('name')
            auditee_comment = form.cleaned_data.get('comment')

            for file in uploaded_files:
                info_required = InformationRequired(
                    audit_program=auditinProgress,  # Associate with the specific audit program
                    name=name,
                    attachments=file,
                    comments=auditee_comment,
                    Chat_room=chat_room
                )
                info_required.save()
                audit_program.uploaded_requirements.add(info_required)

            return render(request, 'fieldwork2/success_page.html')  # Redirect to a success page
    else:
        form = UploadRequirementsForm()

    return render(request, 'fieldwork2/uploadfile.html',
                  {'form': form, 'audit_program': auditinProgress, "requirement_list": requirement_list})


def upload_success(request):
    return render(request, 'fieldwork2/success_page.html')


def chat_room(request):
    return render(request, 'fieldwork2/chatroom.html')


@login_required
def room(request, room_name):
    return render(request, 'fieldwork2/room.html', {'room_name': room_name, 'name': request.user.username})


@login_required
def send_message(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        message = request.POST['message']

        # Send the message to the room using Channels
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            room_name,
            {
                'type': 'chat.message',
                'message': message,
                'username': request.user.username,
            }
        )

        return JsonResponse({'status': 'OK'})
    return JsonResponse({'status': 'FAIL'})
