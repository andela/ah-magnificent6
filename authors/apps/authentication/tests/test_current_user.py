""" module to test current user. """
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authors.apps.authentication.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        """ Setup data for the tests """
        self.user1 = {
            "username": "createduser",
            "email": "createduser@user.user",
            "password": "user123user"
        }
        self.reg_url = reverse('authentication:register')
        self.login_url = reverse('authentication:login')
        self.current_user_url = reverse('authentication:current_user')

        reg = self.client.post(self.reg_url, self.user1, format='json')
        self.login_response = self.client.post(self.login_url, self.user1, format='json')

    def test_successful_current_user(self):
        """ Test successfull current user. Authentication required """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.login_response.data['token'])
        response = self.client.get(self.current_user_url)
        self.assertEqual(response.data['email'], "createduser@user.user")
        self.assertEqual(response.data['username'], "createduser")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsuccessful_inactive_user(self):
        """ Test unsuccessfull current user who is inactive """
        user = User.objects.filter(email=self.user1['email']).first()
        user.is_active = False
        user.save()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                self.login_response.data['token'])
        response = self.client.get(self.current_user_url)
        self.assertEqual(response.data['email'], "createduser@user.user")
        self.assertEqual(response.data['username'], "createduser")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unsuccessful_without_token(self):
        """ Test unsuccessful request without a token """
        response = self.client.get(self.current_user_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
