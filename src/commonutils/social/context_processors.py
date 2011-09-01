from django.contrib.auth.models import AnonymousUser

from .socialize import socialize_user as socialize_user_func

def socialize_user(request):
    if hasattr(request, 'user'):
        if not hasattr(request.user, 'soc_username'):
            user = socialize_user_func(request.user)
        else:
            user = request.user
    else:
        user = AnonymousUser()

    return {
        'user': user,
    }
