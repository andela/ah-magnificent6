import jwt
import datetime

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User


def generate_jwt_token(username):
    """
    This method generates a jwt string with username encoded in it.
    :params str username: A unique name for every user in the system
    :returns: str JWT: A string with username name encoded in it.
    """
    time = datetime.datetime.utcnow() + datetime.timedelta(seconds=86400)
    token = jwt.encode({
        "username": username,
        "exp": time,
    }, settings.SECRET_KEY, algorithm='HS256')

    return token.decode('utf-8')


class JWTAuthentication(authentication.TokenAuthentication):
    """
    Authenticate a receives a token from 'Authorization' Header prepended by
    the keyword 'Bearer'
    Example
     Authorization: Bearer token-str-here.
    """
    keyword = 'Bearer'

    def authenticate_credentials(self, token):
        """
        Decode and check if token is valid and if so, then authenticate the user
        :param token: the token as a string
        :return: Tuple of the user object and non-user authentication
        information
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            try:
                user = User.objects.get(username=payload['username'])
                return user, None
            except User.DoesNotExist:
                return None, None
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Expired Token.')
        except jwt.exceptions.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
