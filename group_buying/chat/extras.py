from django.contrib.auth.models import User
from profiles.models import UserProfile


def profile_exists(user):
    user = User.objects.get(username=user)
    try:
        profile =  user.userprofile
        return True
    except:
        profile = ''
        return False

def get_profile(user):
    if profile_exists(user):
        user = User.objects.filter(username=user).values()[0]
        userprofile = UserProfile.objects.filter(user=user['id']).values()

        return userprofile
def is_admin(user):
    prof = get_profile(user)[0]['is_admin']
    return prof
def is_dealer(user):
    prof = get_profile(user)[0]['is_dealer']
    return prof