from .models import UserProfile
from backend_app.models import Actions, UsageLog


def log_action(action_text, user=None):
    action, _ = Actions.objects.get_or_create(action=action_text)
    UsageLog.objects.create(action=action, user=user)


def get_current_user(request):
    current_user = request.user
    user_profile = UserProfile.objects.get(id=current_user.id)
    return user_profile
