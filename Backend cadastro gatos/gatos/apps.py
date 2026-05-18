import os

from django.apps import AppConfig


class GatosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gatos'

    def ready(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        username = os.environ.get('ADMIN_LOGIN')
        password = os.environ.get('ADMIN_PASSWORD')

        if username and password:
            try:
                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(username=username, email='', password=password)
            except Exception:
                pass