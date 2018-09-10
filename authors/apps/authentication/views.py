from rest_framework import status, generics
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer
)
from .backends import generate_jwt_token


class RegistrationAPIView(generics.CreateAPIView):
    # Use generics.CreateAPIView to show parameters in the API documentation.

    """
    post:
    Register new user

    """

    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        # Separate requests
        email, username, password = request.data.get(
            'email', None), request.data.get(
            'username', None), request.data.get('password', None)

        user = {
            "email": email,
            "username": username,
            "password": password
        }

        """
        The create serializer, validate serializer, save serializer pattern
        below is common and you will see it a lot throughout this course and
        your own work later on. Get familiar with it.
        """
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user_data['token'] = generate_jwt_token(user['username'])

        return Response(user_data, status=status.HTTP_201_CREATED)

    def get(self, request):
        return Response(
            data={"message": 'Only post requests are allowed to this endpoint.'}
        )


class LoginAPIView(generics.GenericAPIView):
    """
    post:
    login existing user.
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):

        email, password = request.data.get(
            'email', None), request.data.get('password', None)

        user = {
            "email": email,
            "password": password
        }

        """
        Notice here that we do not call `serializer.save()` like we did for the
        registration endpoint.
        This is because we don't actually have anything to save.
        Instead, the `validate` method on our serializer
        handles everything we need.
        """
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data

        user_data['token'] = generate_jwt_token(user_data['username'])

        return Response(user_data, status=status.HTTP_200_OK)

    def get(self, request):
        return Response(
            data={"message": 'Only post requests are allowed to this endpoint.'}
        )


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    retrieve:
    Get single user details.

    update:
    Update user details.
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        There is nothing to validate or save here. Instead, we just want the
        serializer to handle turning our `User` object into something that
        can be JSONified and sent to the client.
        """
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
