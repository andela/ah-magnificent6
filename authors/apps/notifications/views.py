"""
This module defines views used in operations for notifications.
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .serializers import NotificationSerializer
from .renderers import NotificationJSONRenderer
from .models import Notification
from authors.apps.profiles.models import Profile


class NotificationDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    delete:
    """
    serializer_class = NotificationSerializer
    renderer_classes = (NotificationJSONRenderer, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        """
        Retrieve a specific notification from the database given it's id.
        :params pk: an id of the notification to retrieve
        :returns notification: a json data for requested notification
        """
        try:
            notification = Notification.objects.get(pk=pk)
            serializer = self.serializer_class(
                notification, context={'request': request})
            return Response(serializer.data, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({
                'error': 'Notification does not exist'
            }, status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """
        Delete a given notification.
        :params pk: an id of the notification to be deleted
                request: a request object with authenticated user credentials
        :returns dict: a json object containing message to indicate that the
        notification has been deleted
        """
        try:
            notification = Notification.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({
                'error': 'Notification with does not exist'
            }, status.HTTP_404_NOT_FOUND)

        #check whether user has the notification before attempting to delete it
        user = request.user
        if user in notification.notified.all():
            notification.notified.remove(user.id)
            message = "You have successfully deleted this notification"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)

        else:
            # prevent a user from deleting an notification they do not own
            return Response({
                'error': 'You cannot delete this notification'
            }, status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        """
        Mark the notification as read.
        The function adds the user id to the read field in the
        Notifications model
        """
        try:
            notification = Notification.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({
                'error': 'Notification with does not exist'
            }, status.HTTP_404_NOT_FOUND)

        #check whether user is in the notified field
        user = request.user
        if user in notification.notified.all():
            notification.read.add(user.id)
            message = "You have successfully marked the notification as read"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({
                'error':
                'You cannot mark as read a notification that is not yours'
            }, status.HTTP_403_FORBIDDEN)


class NotificationAPIView(generics.RetrieveUpdateAPIView):
    """
    get:
    """
    serializer_class = NotificationSerializer
    renderer_classes = (NotificationJSONRenderer, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """
        Retrieve all notifications from the database for a specific user.
        :returns notifications: a json data for the notifications
        """
        user = request.user
        notifications = Notification.objects.all()
        data = {}

        for notification in notifications:
            if user in notification.notified.all():
                serializer = self.serializer_class(
                    notification, context={'request': request})
                data[notification.id] = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Mark all notifications as read.
        """
        notifications = Notification.objects.all()
        user = request.user
        for notification in notifications:
            if user in notification.notified.all():
                notification.read.add(user.id)
                message = "You successfully marked all notifications as read"
                response = {"message": message}
        return Response(response, status=status.HTTP_200_OK)


class NotificationSwitchAPIView(generics.CreateAPIView):
    """
    A user is able to activate or deactivate notifications.
    """
    permission_classes = (IsAuthenticated, )
    # queryset = Profile.objects.all()
    serializer_class = NotificationSerializer

    def post(self, request):
        """
        This method handles activating and deactivating notifications.
        Checks if the user notification boolean is set to true in
        order to deactivate.
        Else activates.
        """
        user = request.user
        profile = Profile.objects.get(user=user)

        if profile.app_notification_enabled is True:
            # sets notification boolean in the profile to false
            profile.notification = False
            profile.save()
            message = "You have successfully deactivated notifications"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)

        else:
            # sets notification boolean in the profile to true
            profile.app_notification_enabled = True
            profile.save()
            message = "You have successfully activated notifications"
            response = {"message": message}
            return Response(response, status=status.HTTP_200_OK)
