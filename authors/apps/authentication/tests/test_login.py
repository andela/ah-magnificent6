""" module to test login. """
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authors.apps.authentication.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        """ Setup data for the tests """
        self.valid_user = {"user": {
            "username": "user1",
            "email": "user1@user.user",
            "password": "user123user"}
        }
        self.registration_url = reverse('authentication:register')
        self.login_url = reverse('authentication:login')
        self.client.post(self.registration_url, self.valid_user, format='json')

    def test_successful_login_user(self):
        """ Test that a user successfully logs in """
        response = self.client.post(
            self.login_url, self.valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertTrue(response.data['token'])

    def test_unsuccessful_login_with_wrong_password(self):
        """ Test unsuccessful log in with a wrong email """
        self.valid_user['user']['password'] = "wrongpassword"
        response = self.client.post(
            self.login_url, self.valid_user, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_not_registered_user_login(self):
        """ Test unsuccessful login for unregistered user. """
        response = self.client.post(
            self.login_url, {
                "email": "unregistered@unreg.unreg",
                "password": "unregistered"
            }, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
