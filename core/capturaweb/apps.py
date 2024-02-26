from django.apps import AppConfig


class CapturawebConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.capturaweb"

    def ready(self):
        import core.capturaweb.signals
        from .views import rehacer_schedule
        rehacer_schedule()
