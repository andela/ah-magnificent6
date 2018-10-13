import jwt
import furl
from requests.exceptions import HTTPError

from rest_framework import status, generics
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, ForgotPasswordSerializer,
    ResetPasswordSerializer, SocialLoginSerializer
)

from .backends import generate_jwt_token
from .models import User
from authors.apps.core.mailer import SendMail

# social authentication packages
from social_django.utils import load_strategy, load_backend

from social_core.exceptions import MissingBackend

from social.backends.oauth import BaseOAuth1, BaseOAuth2


class RegistrationAPIView(generics.CreateAPIView):
    # Use generics.CreateAPIView to show parameters in the API documentation.
    """
    post:
    Register new user.

    get:
    Get appropriate error on get.
    """

    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        # Separate requests
        email, username, password = request.data.get(
            'email', None), request.data.get('username',
                                             None), request.data.get(
            'password', None)

        user = {"email": email, "username": username, "password": password}
        """
        The create serializer, validate serializer, save serializer pattern
        below is common and you will see it a lot throughout this course and
        your own work later on. Get familiar with it.
        """
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        # sends email with the activation link with the token
        subject = 'Authors Haven activation email'
        message = "Click this link to be activated "
        domain = get_current_site(request).domain
        token = generate_jwt_token(user['username'])
        protocol = request.META['SERVER_PROTOCOL'][:4]

        activation_link = protocol + '://' + domain + '/api/auth/' + token

        try:
            send_mail(
                subject,
                message + activation_link,
                settings.EMAIL_HOST_USER, [user['email']],
                fail_silently=False)
        except:
            return Response(data={"message": "Email activation failed"})

        serializer.save()
        data = {
            "message":
                "Kindly click the link sent to your email to complete registration."
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request):
        return Response(
            data={
                "message": 'Only post requests are allowed to this endpoint.'
            })


class LoginAPIView(generics.GenericAPIView):
    """
    post:
    Login existing user.

    get:
    Show appropriate error on get.
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        email, password = request.data.get('email', None), request.data.get(
            'password', None)

        user = {"email": email, "password": password}
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
            data={
                "message": 'Only post requests are allowed to this endpoint.'
            })


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
        serializer_data = {
            'username': serializer_data.get('username', request.user.username),
            'email': serializer_data.get('email', request.user.email),
            'profile': {
                'first_name': serializer_data.get('first_name', request.user.profile.first_name),
                'last_name': serializer_data.get('last_name', request.user.profile.last_name),
                'birth_date': serializer_data.get('birth_date', request.user.profile.birth_date),
                'bio': serializer_data.get('bio', request.user.profile.bio),
                'avatar': serializer_data.get('avatar', request.user.profile.avatar),
                'city': serializer_data.get('city', request.user.profile.city),
                'country': serializer_data.get('country', request.user.profile.country),
                'phone': serializer_data.get('phone', request.user.profile.phone),
                'website': serializer_data.get('website', request.user.profile.website),
            }
        }

        # Here is that serialize, validate, save pattern we talked about before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ForgotPasswordAPIView(APIView):
    """Forget password view captures email and generates token that will be.
    used during reset password. Data that is captures in the view is send to
    the serializer class
    Post:
    Forgot password
    """
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        """Forgot password"""

        # Query for email in database
        user = User.objects.filter(email=request.data['email']).first()
        if user is None:
            return Response({"message": "The email you entered does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Get URL for client and include in the email for resetting password
        current_site_domain = request.META['HTTP_ORIGIN']
        # generate token
        token = default_token_generator.make_token(user)
        reset_link_url = furl.furl(
            '{}/reset-password/'.format(current_site_domain))
        reset_link_url.args = (('token', token), ('email', user.email))

        # Sends mail with url, path of reset password and token
        mail_message = 'Dear {},\n\nWe received a request to change your\
        password on Authors Haven.\n\nClick the link below to set a new\
        password.\n{}\
        \n\nYours\n AuthorsHaven.'.format(user.username, reset_link_url)

        SendMail(subject="Reset Password",
                 message=mail_message,
                 email_from='magnificent6ah@gmail',
                 to=user.email).send()

        output = {"message": "Please check your email for further instruction"}

        return Response(output, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    """Reset password view allows any user to access reset password endpoint
        and updates password
        put:
        Reset user password
    """

    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def put(self, request, token):
        """Reset password
        """
        data = request.data
        data["token"] = token
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        output = {"message": "Your password has been successfully changed"}
        return Response(output, status=status.HTTP_200_OK)


class UserActivationAPIView(APIView):
    """
    Activate account using the link sent to the user's email.

    Decodes the token in the url and confirms whether the user
    is in the database using the username in the token.
    If successful, the user's account is activated.
    """
    renderer_classes = (UserJSONRenderer,)

    def get(self, request, token):
        try:
            data = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(username=data['username'])
        except:
            return Response(
                data={"message": "Activation link is invalid."},
                status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return Response(
            data={"message": "Account was verified successfully"},
            status=status.HTTP_200_OK)


class SocialLoginView(generics.CreateAPIView):
    """ Allows login through social sites like Google, Twitter and Facebook """
    permission_classes = (AllowAny,)
    serializer_class = SocialLoginSerializer
    renderer_classes = (UserJSONRenderer,)

    def create(self, request):
        """ Receives a provider and token and creates a new user,
            if the new user does not exist already.
            The username is retreived and used to generate the JWT token
            used to access the apps endpoints.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = serializer.data.get("provider")

        # If request is from existing user, associate social account with it
        existing_user = request.user if not request.user.is_anonymous else None

        # Load Django code to plug into Python Social Auth's functionality
        strategy = load_strategy(request)
        try:
            # Get backend corresponding to provider.
            backend = load_backend(
                strategy=strategy, name=provider, redirect_uri=None)

            if isinstance(backend, BaseOAuth1):
                # Get access_token and access token secret for Oauth1 used by Twitter
                if "access_token_secret" in request.data:
                    access_token = {
                        'oauth_token': request.data['access_token'],
                        'oauth_token_secret': request.data['access_token_secret']
                    }
                else:
                    return Response(
                        {"error": "Provide access token secret"}, status=status.HTTP_400_BAD_REQUEST
                    )

            elif isinstance(backend, BaseOAuth2):
                # Get access token for OAuth2
                access_token = serializer.data.get("access_token")

        except MissingBackend:
            return Response({"error": "Invalid provider"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = backend.do_auth(access_token, user=existing_user)
        except BaseException as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        # Activate user since they have used social auth so no need for email activation
        if not user.is_active:
            user.is_active = True
            user.save()

        # Serialize the user.
        serializer = UserSerializer(user)

        user_data = serializer.data
        # Grant user app's access_token
        user_data["token"] = generate_jwt_token(user_data["username"])

        return Response(user_data, status=status.HTTP_200_OK)
