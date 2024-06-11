from django.apps import AppConfig

class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "your_app_name"  # replace 'your_app_name' with the actual name of your app

    def ready(self):
        """
        Import any models or perform any other setup here.
        """
        try:
            import your_app_name.signals  # replace 'your_app_name' with the actual name of your app
        except ImportError:
            pass
