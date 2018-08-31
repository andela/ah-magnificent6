import jwt
import datetime

from django.conf import settings


def generate_jwt_token(email, username):
    """Method to generate user jwt token."""
    time = datetime.datetime.utcnow() + datetime.timedelta(seconds=86400)
    token = jwt.encode({
        "username": username,
        "exp": time,
    }, settings.SECRET_KEY, algorithm='HS256')

    return token.decode('utf-8')
