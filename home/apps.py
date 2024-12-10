from django.apps import AppConfig

class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"  # Changed from "your_app_name" to "home"

    def ready(self):
        """
        Import any models or signals here.
        """
        try:
            import home.signals
        except ImportError:
            pass
