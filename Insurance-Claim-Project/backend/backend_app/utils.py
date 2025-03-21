from .models import UserProfile


def get_current_user(request):
    current_user = request.user
    user_profile = UserProfile.objects.get(id=current_user.id)
    return user_profile
