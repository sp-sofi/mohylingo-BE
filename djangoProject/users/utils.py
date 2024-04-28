from rest_framework.authtoken.models import Token
from rest_framework import exceptions

def get_user_from_token(key):
    try:
        token = Token.objects.get(key=key)
        return token.user
    except Token.DoesNotExist:
        raise exceptions.AuthenticationFailed('Invalid token')

def get_user_from_auth_request(request):
    token_key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    user = get_user_from_token(token_key)
    return user