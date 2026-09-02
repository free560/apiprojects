from django.apps import AppConfig

class AccountApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account_api'

    def ready(self):
        import account_api.signals