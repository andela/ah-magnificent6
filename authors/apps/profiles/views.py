from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.response import Response

from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer
from authors.apps.authentication.serializers import UserSerializer
from authors.apps.authentication.models import User


class FollowAPIView(APIView):
    """ This class contains method for following and unfollowing a user

    post:
    Follow a user.

    delete:
    Un-follow a user

    """

    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def post(self, request, username):
        """ This method enables a user to follow another user """

        # current user
        follower = request.user.profile

        # check if the user to be followed in the database
        try:
            followed = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('The user you are looking for does not exist')

        # Check if user is same
        if follower.pk is followed.pk:
            raise ValidationError("You cannot follow yourself")

        # Add user
        follower.follow(followed)

        serialize = self.serializer_class(follower, context={'request': request})
        return Response(data=serialize.data, status=status.HTTP_200_OK)

    def delete(self, request, username):
        """ This method enables a user to un-follow another user """

        # current user
        follower = request.user.profile

        # check if the user to be followed in the database
        try:
            followed = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('The user you are looking for does not exist')

        # Check if user is same
        if follower.pk is followed.pk:
            raise ValidationError("You cannot perform that action")

        follower.unfollow(followed)

        serialize = self.serializer_class(follower, context={'request': request})
        return Response(data=serialize.data, status=status.HTTP_200_OK)


class FollowersAPIView(APIView):
    """ This class contains method that retrieve all following users
    Get:
    Followers

    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request, username):
        """ This method get a user followers"""

        user = request.user.profile
        profile = Profile.objects.get(user__username=username)

        follower = user.followers(profile)

        serializer = self.serializer_class(follower, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowingAPIView(APIView):
    """ This class contains method that retrieve all following user"""
    permission_classes = (IsAuthenticated,)

    serializer_class = ProfileSerializer

    def get(self, request, username):
        """ This method gets all following users"""

        user = request.user.profile
        profile = Profile.objects.get(user__username=username)

        following = user.following(profile)
        serializer = self.serializer_class(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
