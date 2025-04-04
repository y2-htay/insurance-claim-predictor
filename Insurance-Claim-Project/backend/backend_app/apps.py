from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # Set model id fields as 64-bit integers (unless overridden)
    name = 'backend_app'

    def ready(self):
        UserProfile = get_user_model()
        try:
            if not UserProfile.objects.filter(username="user").exists():
                UserProfile.objects.create(
                    username="user",
                    password=make_password("hashyPass"),
                    permission_level=0
                )
        except IntegrityError:
            pass  # Ignore if user already exists