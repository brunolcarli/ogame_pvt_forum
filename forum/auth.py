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
        user_id = kwargs['user_id']
        try:
            user = CustomUser.objects.get(username=token_user, id=user_id)
        except CustomUser.DoesNotExist:
            raise Exception('AUTH ERROR: Invalid credentials for this user')

        # TODO: check if user is banned or blocked

        return function(*args, **kwargs)
    return decorated