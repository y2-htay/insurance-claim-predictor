from backend_app.models import Actions, UsageLog


def log_action(action_text, user):
    action, _ = Actions.objects.get_or_create(action=action_text)
    UsageLog.objects.create(action=action, user=user)
