from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import AuditorRegistrationForm, AuditeeRegistrationForm
from .models import Auditor, Auditee


def home(request):
    return render(request, 'audit_plan_setup/home.html')


def register_auditor(request):
    if request.method == 'POST':
        form = AuditorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Auditor.objects.create(name=user)
            login(request, user)
            return redirect('home')  # Redirect to the home page or another page
    else:
        form = AuditorRegistrationForm()
    return render(request, 'audit_plan_setup/register_auditor.html', {'form': form})


def register_auditee(request):
    if request.method == 'POST':
        form = AuditeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Auditee.objects.create(user=user)
            login(request, user)
            return redirect('home')  # Redirect to the home page or another page
    else:
        form = AuditeeRegistrationForm()
    return render(request, 'audit_plan_setup/register_auditee.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'audit_plan_setup/login.html'
