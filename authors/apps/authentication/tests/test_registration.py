""" module to test registration. """
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authors.apps.authentication.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        """ Setup data for the tests """
        self.user1 = { 
            "username": "user1",
            "email": "user1@user.user",
            "password": "user123user"
        }
        self.reg_url = reverse('authentication:register')


    def test_successful_registered_user(self):
        """ Test that a user is successfully registered. """
        users = User.objects.count()
        response = self.client.post(self.reg_url, self.user1, format='json')
        self.assertEqual(response.data['email'], self.user1['email'])
        self.assertEqual(response.data['username'], self.user1['username'])
        self.assertEqual(User.objects.count(), (users+1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsuccessful_register_existing_user(self):
        """ Test that one cannot register twice with same credentials """
        self.client.post(self.reg_url, self.user1, format='json')
        response = self.client.post(self.reg_url, self.user1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_register_without_user_name(self):
        """ Test user cannot register without a username. """
        self.user1['username'] = ""
        response1 = self.client.post(self.reg_url, self.user1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_register_empty_user_name(self):
        """ Test that a user cannot register empty string. """
        self.user1['username'] = " "
        response = self.client.post(self.reg_url, self.user1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_register_with_email_wrong_format(self):
        """ Test that the user enters an email in the correct format """
        self.user1['email'] = "wrongformatemail"
        response = self.client.post(self.reg_url, self.user1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_registration_empty_email(self):
        """ Test that the user does not enter an empty email """
        self.user1['email'] = ""
        response = self.client.post(self.reg_url, self.user1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_registration_with_weak_password(self):
        """ Test that a user enters a weak password with less characters """
        self.user1['password'] = "1234"
        response = self.client.post(self.reg_url, self.user1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_registration_without_password(self):
        """ Test that a user enters no password """
        self.user1['password'] = ""
        response = self.client.post(self.reg_url, self.user1, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
