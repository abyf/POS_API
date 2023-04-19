from django.apps import AppConfig


class PosApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pos_api'

    def ready(self):
        import pos_api.signals
