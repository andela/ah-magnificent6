"""Module to test reset password"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator


class ResetPassword(APITestCase):
    def setUp(self):
        """Set the data for test"""
        self.email = {"email": "michael.nthiwa@andela.com"}
        self.valid_user = {
            "username": "michael",
            "email": "michael.nthiwa@andela.com",
            "password": "123456789"}

        self.client.post(reverse('authentication:register'), self.valid_user, format='json')
        self.forget_password_url = reverse('authentication:forgot')

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

    def test_reset_password(self):
        """Test user successfully reset password"""

        user = get_user_model().objects.create_user(username='leon', email='leon.kioko@andela.com',
                                                    password='123456789')
        token = default_token_generator.make_token(user)
        reset_password_url = reverse('authentication:reset_password', kwargs={'token': token })

        new_password = {"password": "abcdef",
                        "confirm_password": "abcdef",
                        "email": "leon.kioko@andela.com",
                        "token": token}
        response = self.client.put(reset_password_url, data=new_password, format='json')
        self.assertIn('Your password has been successfully changed', str(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


