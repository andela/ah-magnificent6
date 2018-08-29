""" module to test login. """
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authors.apps.authentication.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        """ Setup data for the tests """
        self.user1 = {
            "username": "createduser1",
            "email": "createduser1@user.user",
            "password": "user123user"
        }
        self.registration_url = reverse('authentication:register')
        self.login_url = reverse('authentication:login')
        reg = self.client.post(self.registration_url, self.user1, format='json')

    def test_successful_login_user(self):
        """ Test that a user successfully logs in """
        response = self.client.post(self.login_url, self.user1, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_201_CREATED)

    def test_unsuccessful_login_with_wrong_password(self):
        """ Test unsuccessful log in with a wrong email """
        self.user1['password'] = "wrongpassword"
        response = self.client.post(self.login_url, self.user1, format='json')
        self.assertEqual(login_response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_not_registered_user_login(self):
        """ Test unsuccessful login for unregistered user. """
        response = self.client.post(
            self.login_url, {
                "email": "unregistered@unreg.unreg",
                "password": "unregistered"
            }, format='json')
        self.assertEqual(login_response.status_code,
                         status.HTTP_400_BAD_REQUEST)
