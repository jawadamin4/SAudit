from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import register_auditor, register_auditee, home, CustomLoginView

urlpatterns = [
    path('', home, name='home'),
    path('register/auditor/', register_auditor, name='register_auditor'),
    path('register/auditee/', register_auditee, name='register_auditee'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    # Add other URLs as needed
]
