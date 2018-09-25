from .base_setup import Base
from rest_framework import status
from django.urls import reverse
from django.core import mail

from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile
from authors.apps.core.cron import EmailNotificationCron


class ArticleDeleteUpdateTests(Base):
    """Test suite for favouriting articles."""

    def setUp(self):
        """Setup data for the tests."""
        super().setUp()
        self.res = self.client.post(
            self.article_url,
            self.article_data,
            format="json",
            **self.headers_one)

    def tearDown(self):
        """Teardown for the tests."""
        super().tearDown()

    def test_successfull_notification(self):
        """
        Tests that a user successfully receiving notifications.
        """
        notification = self.client.get(
            reverse('notifications:my_notifications'), **self.headers_two)
        self.assertEqual(notification.status_code, status.HTTP_200_OK)

    def test_successfully_get_a_notification(self):
        """
        Tests that a user can get a notification.
        """
        EmailNotificationCron().do()
        self.assertEqual(len(mail.outbox), 3)
        notification = self.client.get(
            reverse('notifications:my_notifications'), **self.headers_two)
        pk = [*notification.data][0]
        response = self.client.get(
            reverse('notifications:notification', kwargs={'pk': pk}),
            **self.headers_two)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successfully_delete_notification(self):
        """
        Tests that a user can delete a notification.
        """
        notification = self.client.get(
            reverse('notifications:my_notifications'), **self.headers_two)
        pk = [*notification.data][0]
        delete = self.client.delete(
            reverse('notifications:notification', kwargs={'pk': pk}),
            **self.headers_two)
        self.assertEqual(delete.status_code, status.HTTP_200_OK)

    def test_unsuccessfully_delete_notification(self):
        """
        Tests that a user cannot delete a notification they do not own.
        """
        notification = self.client.get(
            reverse('notifications:my_notifications'), **self.headers_two)
        pk = [*notification.data][0]
        delete = self.client.delete(
            reverse('notifications:notification', kwargs={'pk': pk}),
            **self.headers_one)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)

    def test_unsuccessfully_mark_read_notification(self):
        """
        Tests that a user cannot mark read a notification they do not own.
        """
        notification = self.client.get(
            reverse('notifications:my_notifications'), **self.headers_two)
        pk = [*notification.data][0]
        delete = self.client.put(
            reverse('notifications:notification', kwargs={'pk': pk}),
            **self.headers_one)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)

    def test_successfully_mark_read_notification(self):
        """
        Tests that a user successfully marks as read.
        """
        notification = self.client.get(
            reverse('notifications:my_notifications'), **self.headers_two)
        pk = [*notification.data][0]
        delete = self.client.put(
            reverse('notifications:notification', kwargs={'pk': pk}),
            **self.headers_two)
        self.assertEqual(delete.status_code, status.HTTP_200_OK)

    def test_unsuccessfully_mark_read_notification(self):
        """
        Tests that a user cannot mark as read a notification they do not own.
        """
        notification = self.client.get(
            reverse('notifications:my_notifications'), **self.headers_two)
        pk = [*notification.data][0]
        delete = self.client.put(
            reverse('notifications:notification', kwargs={'pk': pk}),
            **self.headers_one)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)

    def test_successfully_mark_all_notification_as_read(self):
        """
        Tests that a user successfully marks all as read.
        """
        notification = self.client.put(
            reverse('notifications:my_notifications'), **self.headers_two)
        self.assertEqual(notification.status_code, status.HTTP_200_OK)
        response = self.client.get(
            reverse('notifications:my_notifications'), **self.headers_two)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsuccessfully_mark_non_existing_notification(self):
        """
        Tests that a user unssuccessful marks as read non existing notification.
        """
        response = self.client.put(
            reverse('notifications:notification', kwargs={'pk': 500}),
            **self.headers_two)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unsuccessfully_delete_non_existing_notification(self):
        """
        Tests that a user unsuccessfully deletes non-existing notification.
        """
        response = self.client.delete(
            reverse('notifications:notification', kwargs={'pk': 500}),
            **self.headers_two)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unsuccessfully_get_non_existing_notification(self):
        """
        Tests that a user unsuccessfully gets non-existing notification.
        """
        response = self.client.get(
            reverse('notifications:notification', kwargs={'pk': 500}),
            **self.headers_two)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_successfully_activate_app_notification(self):
        """
        Tests that a user successfully activating notifications.
        """
        response = self.client.post(
            reverse('notifications:switch_app_notifications'),
            **self.headers_two)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successfully_deactivate_app_notification(self):
        """
        Tests that a user successfully deactivating notifications.
        """
        self.client.post(
            reverse('notifications:switch_app_notifications'),
            **self.headers_one)
        response = self.client.post(
            reverse('notifications:switch_app_notifications'),
            **self.headers_one)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successfully_activate_email_notification(self):
        """
        Tests that a user successfully activating notifications.
        """
        response = self.client.post(
            reverse('notifications:switch_email_notifications'),
            **self.headers_two)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successfully_deactivate_email_notification(self):
        """
        Tests that a user successfully deactivating notifications.
        """
        self.client.post(
            reverse('notifications:switch_email_notifications'),
            **self.headers_one)
        response = self.client.post(
            reverse('notifications:switch_email_notifications'),
            **self.headers_one)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
