from .models import UserProfile

# This is show the user profile picture in every page
def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = None
        return {'user_profile': profile}
    return {}
