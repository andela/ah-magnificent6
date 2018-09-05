from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile

class ProfileTests(APITestCase):
    def setUp(self):
        """ Setup data for the tests """
        self.user_data = { "user": {
            "username": "John",
            "email": "john@company.com",
            "password": "john1234",
            "bio": "I am a test user",
            "image": "image-url",
            "following": False }
        }
        self.registration_url = reverse('authentication:register')
    
    def test_create_profile(self):
        """
        Ensure we can create a new profile object.
        """
        curr_users = User.objects.count()
        response = self.client.post(self.registration_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), (curr_users+1))
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().bio, 'I am a test user')
