from django.apps import AppConfig

class Fieldwork2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fieldwork2'
    verbose_name = '6-Fieldwork'

    def ready(self):
        import fieldwork2.signals