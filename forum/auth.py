from datetime import datetime
from functools import wraps
from graphql_jwt import Verify
from forum.models import CustomUser


def access_required(function):
    """
    Check if the user is logged on the system.
    """
    @wraps(function)
    def decorated(*args, **kwargs):
        token = args[1].context.META.get('HTTP_AUTHORIZATION')
        if not token:
            raise Exception('Unauthorized')
        try:
            _, token = token.split('Bearer ')
        except:
            raise Exception('Invalid authorization method')

        validator = Verify.Field()
        try:
            payload = validator.resolver(None, args[1], token).payload
        except:
            raise Exception('Unauthorized')

        token_exp = datetime.fromtimestamp(payload['exp'])
        now = datetime.now()
        if token_exp < now:
            raise Exception('Session expired')

        token_user = payload['username']
        username = kwargs['username']

        if token_user != username:
            raise Exception('AUTH ERROR: Invalid credentials for this user')

        try:
            user = CustomUser.objects.get(username=token_user)
        except CustomUser.DoesNotExist:
            raise Exception('AUTH ERROR: Invalid credentials for this user')

        if user.is_banned:
            raise Exception('AUTH ERROR: banned users cannot perform actions')

        # inject user id on kwargs
        kwargs['user_id'] = user.id

        return function(*args, **kwargs)
    return decorated
