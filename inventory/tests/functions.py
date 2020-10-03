def _user_for(user_or_profile):
    if type(user_or_profile) == Profile:
        user = user_or_profile.user_object
    elif type(user_or_profile) == User:
        user = user_or_profile
    else:
        raise ValueError("this function requires a Profile or User")
    return user

def login_as(user, testcase):
    user.set_password('foo')
    user.save()
    testcase.client.login(username=user.username,
                          email=user.email,
                          password='foo')
