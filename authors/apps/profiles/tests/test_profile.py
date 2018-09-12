from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authors.apps.authentication.backends import generate_jwt_token
from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile

class ProfileTests(APITestCase):
    def setUp(self):
        """ Setup data for the tests """
        self.user_data = {
                "username": "John",
                "email": "john@company.com",
                "password": "john1234"
            }
        self.profile_data = {
            	"user": {
                    "email": "joe3@company.com",
                    "first_name": "Joe",
                    "last_name": "Doe",
                    "birth_date": "1970-03-04",
                    "bio": "hI I am Joe",
                    "city": "Nairobi",
                    "country": "Kenya",
                    "avatar":  "http://www.google.com",
                    "phone": "21474836",
                    "website": "http://www.google.com"
                }
            }
        self.registration_url = reverse('authentication:register')
        self.login_url = reverse('authentication:login')
        self.profile_url = reverse('authentication:current_user')

    def test_create_profile(self):
        """
        Ensure we can create a new profile object.
        """
        curr_users = User.objects.count()
        response = self.client.post(self.registration_url, self.user_data, format='json')        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), (curr_users+1))
        self.assertEqual(Profile.objects.count(), 1)

    def test_update_profile(self):
        """
        Ensure we can update a profile object.
        """
        register_user = self.client.post(self.registration_url, self.user_data, format='json')
        token = generate_jwt_token(self.user_data['username'])
        activate_user = self.client.get(reverse("authentication:activate_user", args=[token]))
        login_response = self.client.post(self.login_url, self.user_data, format='json')
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(login_response.data.get('token'))}
        profile_response = self.client.put(self.profile_url, self.profile_data, format='json', **headers)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data.get('city'), self.profile_data.get('city'))
