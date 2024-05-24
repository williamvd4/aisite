from django.apps import AppConfig

class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_name"  # replace 'app_name' with the actual name of the app

    def ready(self):
        # import any models or perform any other setup here
        from . import signals  # replace 'signals' with the actual name of the signals module, if any

