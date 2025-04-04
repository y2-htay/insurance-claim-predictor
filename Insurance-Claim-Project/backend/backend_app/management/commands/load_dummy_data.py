from django.core.management.base import BaseCommand
from accounts.models import UserProfile
from django.contrib.auth.hashers import make_password
import json

class Command(BaseCommand):
    help = 'Loads dummy user data into the database'

    def handle(self, *args, **kwargs):
        # Create dummy user
        user = UserProfile.objects.create(
            username="user",
            password=make_password('needsHash'),  # Hash the password
            permission_level=0
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created user {user.username}'))