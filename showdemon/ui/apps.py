from django.apps import AppConfig


class UiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ui'

    def ready(self):
        from ui.main import start_app
        start_app()
        # from ui.examples import example1
        # example1()
