from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authors.apps.authentication.models import User
from django.core import mail
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from authors.apps.authentication.backends import generate_jwt_token, JWTAuthentication


class VerifyTestCase(TestCase):
    """Test suite for registration verification."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = {
            "username": "user1",
            "email": "user1@user.user",
            "password": "user123user"
        }
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.registration_url = reverse('authentication:register')

    def test_email_sent(self):
        """Test if email has been sent and has verification content."""
        response = self.client.post(
            '/api/users/signup/', self.user, format='json')
        self.assertEqual(len(mail.outbox), 1)

    def test_account_is_verified(self):
        """Test user verifying their account from link sent in email."""
        registration = self.client.post(
            self.registration_url, self.user, format='json')
        token = generate_jwt_token(self.user['username'])
        response = self.client.get(
            reverse("authentication:activate_user", args=[token]))
        user = User.objects.get(username=self.user['username'])
        self.assertTrue(user.is_active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_existing_user_token(self):
        """Test unsuccessful token verification."""
        token = generate_jwt_token('username')
        response = JWTAuthentication()
        self.assertEqual(
            response.authenticate_credentials(token), (None, None))

    def test_invalid_activation_link(self):
        """Test invalid activation link."""
        registration = self.client.post(
            self.registration_url, self.user, format='json')
        token = generate_jwt_token(self.user['username'])
        wrong_token = token + "34rhnv"
        response = self.client.get(
            reverse("authentication:activate_user", args=[wrong_token]))
        user = User.objects.get(username=self.user['username'])
        self.assertFalse(user.is_active)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
