import re
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.mail import send_mail


from django.contrib.auth.tokens import default_token_generator
from .models import User
from .backends import generate_jwt_token
from authors.apps.profiles.serializers import ProfileSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    # Serializers registration requests and creates a new user.ß

    """
    Ensure passwords are at least 8 characters long, no longer than 128
    characters, and can not be read by the client.
    """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    """
    Ensure that the email entered is unique and give a descriptive
    error message if a duplicate email is entered
    """
    email = serializers.EmailField(
        validators=[UniqueValidator(
            User.objects.all(), 'That email is already used. '
            'Sign in instead or try another')]
    )

    """
    Ensure that the username entered is unique and give a descriptive
    error message if a duplicate username is entered
    """
    username = serializers.CharField(
        validators=[UniqueValidator(
            User.objects.all(), 'That username is taken. Please try another')]
    )

    """
    The client should not be able to send a token along with a registration
    request. Making `token` read-only handles that for us.
    """
    class Meta:
        # RegistrationSerializer uses User model
        model = User

        """
        List all of the fields that could possibly be included in a request
        or response, including fields specified explicitly above.
        """
        fields = ['email', 'username', 'password']

    def validate(self, data):
        """
        The `validate` method is where we make sure that the current
        instance of `RegistrationSerializer` has "valid". In the case of registering
        a user, this means validating that they've provided an email, username
        and password.
        """
        password = data.get('password', None)

        """
        Ensure that a password is alphanumeric, that is, it has both numbers and letters
        """
        if not re.match(r'^(?=.*[a-zA-Z])(?=.*[0-9]).*', password):
            raise serializers.ValidationError(
                'Invalid password. Please choose a password with at least a '
                'letter and a number.'
            )

        return data

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)

    def __init__(self, *args, **kwargs):
        super(RegistrationSerializer, self).__init__(*args, **kwargs)

        # Override the error_messages of each field with a custom error message
        for field in self.fields:
            field_error_messages = self.fields[field].error_messages
            field_error_messages['null'] = field_error_messages['blank'] \
                = field_error_messages['required'] \
                = 'Please fill in the {}'.format(field)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        """
        The `validate` method is where we make sure that the current
        instance of `LoginSerializer` has "valid". In the case of logging a
        user in, this means validating that they've provided an email
        and password and that this combination matches one of the users in
        our database.
        """
        email, password = data.get('email', None), data.get('password', None)

        """
        As mentioned above, an email is required. Raise an exception if an
        email is not provided.
        """
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        """
        As mentioned above, a password is required. Raise an exception if a
        password is not provided.
        """
        if not password:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        """
        The `authenticate` method is provided by Django and handles checking
        for a user that matches this email/password combination. Notice how
        we pass `email` as the `username` value. Remember that, in our User
        model, we set `USERNAME_FIELD` as `email`.
        """
        user = authenticate(username=email, password=password)

        """
        If no user was found matching this email/password combination then
        `authenticate` will return `None`. Raise an exception in this case.
        """
        if not user:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        """
        Django provides a flag on our `User` model called `is_active`. The
        purpose of this flag to tell us whether the user has been banned
        or otherwise deactivated. This will almost never be the case, but
        t is worth checking for. Raise an exception in this case.
        """
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        token = generate_jwt_token(email)

        """
        The `validate` method should return a dictionary of validated data.
        This is the data that is passed to the `create` and `update` methods
        that we will see later on.
        """
        return {
            'email': user.email,
            'username': user.username,
            'token': token

        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    """
    Passwords must be at least 8 characters, but no more than 128 
    characters. These values are the default provided by Django. We could
    change them, but that would create extra work while introducing no real
    benefit, so let's just stick with the defaults.
    """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'profile')

        """
        The `read_only_fields` option is an alternative for explicitly
        specifying the field with `read_only=True` like we did for password
        above. The reason we want to use `read_only_fields` here is because
        we don't need to specify anything else about the field. For the
        password field, we needed to specify the `min_length` and
        `max_length` properties too, but that isn't the case for the token
        field.
        """

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        """
        Passwords should not be handled with `setattr`, unlike other fields.
        This is because Django provides a function that handles hashing and
        salting passwords, which is important for security. What that means
        here is that we need to remove the password field from the
        `validated_data` dictionary before iterating over it.
        """
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile')

        for (key, value) in validated_data.items():
            """
            For the keys remaining in `validated_data`, we will set them on
            the current `User` instance one at a time.
            """
            setattr(instance, key, value)
        
        for (key, value) in profile_data.items():
            """
            For the keys in `profile_data`, we will set them on
            the current `User` instance one at a time.
            """
            setattr(instance.profile, key, value)

        if password is not None:
            """
            `.set_password()` is the method mentioned above. It handles all
            of the security stuff that we shouldn't be concerned with.
            """
            instance.set_password(password)

        """
        Finally, after everything has been updated, we must explicitly save
        the model. It's worth pointing out that `.set_password()` does not
        save the model.
        """
        instance.save()

        """
        Save the user profile after update
        """
        # instance.profile.save()

        return instance


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer for forget password"""

    email = serializers.CharField(max_length=255)


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for reset password"""

    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255)

    def validate(self, data):
        """Validates passwords and token.
        Token can only be used once"""

        # Query DB for user email
        user = User.objects.filter(email=data.get('email', None)).first()

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")

        # Checks token generated is valid
        is_valid_token = default_token_generator.check_token(user, data.get('token', None))
        if is_valid_token is False:
            raise serializers.ValidationError("Token is Invalid or it has already expired")

        user.set_password(data.get('password'))
        user.save()

        return data
        
class SocialLoginSerializer(serializers.Serializer):
    """ Accept OAUTH access token and provider.
        Oauth produces its own access token.
        "provider" is used to determine the source of the social login.
    """

    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)
    access_token_secret = serializers.CharField(max_length=4096, required=False, trim_whitespace=True)




