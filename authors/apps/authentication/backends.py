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
    pass
