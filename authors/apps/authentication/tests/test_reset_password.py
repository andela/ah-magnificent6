"""Module to test reset password"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ResetPassword(APITestCase):
    def setUp(self):
        """Set the data for test"""
        self.email = {"email": "michael.nthiwa@andela.com"}
        self.valid_user = {"user": {
            "username": "michael",
            "email": "michael.nthiwa@andela.com",
            "password": "123456789"}
        }
        self.client.post(reverse('authentication:register'), self.valid_user, format='json')
        self.forget_password_url = reverse('authentication:forgot')
        self.reset_password_url = reverse('authentication:reset_password')

    def test_sending_successful_email(self):
        """Test email is sent"""

        response = self.client.post(self.forget_password_url, self.email, format='json')
        self.assertIn('Please confirm your email for further instruction', str(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_email(self):
        """Test for invalid email"""

        email = {"email": "michael@andela.com"}
        response = self.client.post(self.forget_password_url, email, format='json')
        self.assertIn('The email you entered does not exist', str(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
