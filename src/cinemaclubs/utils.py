from social_auth.models import UserSocialAuth

def get_social_link(provider, uid):
    if provider == 'openid':
        return uid
    elif provider == 'facebook':
        return 'https://www.facebook.com/profile.php?id=%s' % uid
    return ''

def socialize_users(*users_list):
    '''
    Adds to each user in @users_list social attributes:
    soc_provider, soc_uid, soc_link

    @users_list is modified
    '''
    soc_auths = UserSocialAuth.objects.filter(user__in=users_list)
    soc_auths_by_users = {soc_auth.user.id:soc_auth for soc_auth in soc_auths}

    for user in users_list:
        user_soc_auth = soc_auths_by_users.get(user.id)
        if user_soc_auth:
            user.soc_provider = user_soc_auth.provider
            user.soc_uid = user_soc_auth.uid
            user.soc_link =  get_social_link(user.soc_provider, user.soc_uid)
        else:
            user.soc_provider = None
            user.soc_uid = 0
            user.soc_link = ''
