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
        self.user_data2 = {
            "username": "jane",
            "email": "jane@company.com",
            "password": "jane1234"
        }

        self.profile_data = {
            "user": {
                "username": "joe",
                "email": "joe3@company.com",
                "first_name": "Joe",
                "last_name": "Doe",
                "birth_date": "1970-03-04",
                "bio": "hI I am Joe",
                "city": "Nairobi",
                "country": "Kenya",
                "avatar": "http://www.google.com",
                "phone": "21474836",
                "website": "http://www.google.com"
            }
        }
        self.registration_url = reverse('authentication:register')
        self.login_url = reverse('authentication:login')
        self.profile_url = reverse('authentication:current_user')
        self.follow_url = reverse('profiles:follow', kwargs={"username": self.user_data2["username"]})
        self.following_url = reverse('profiles:following', kwargs={"username": self.user_data["username"]})
        self.followers_url = reverse('profiles:followers', kwargs={"username": self.user_data2["username"]})
        self.profiles_url = reverse('profiles:profiles')
        self.user_response = self.client.post(self.registration_url, self.user_data, format='json')
        self.client.post(self.registration_url, self.user_data2, format='json')
        token = generate_jwt_token(self.user_data['username'])
        self.client.get(reverse("authentication:activate_user", args=[token]))

    def test_create_profile(self):
        """
        Ensure we can create a new profile object.
        """
        curr_users = User.objects.count()
        self.assertEqual(self.user_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), curr_users)
        self.assertEqual(Profile.objects.count(), 2)

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

    def test_follow_user(self):
        """
        Ensure user can follow another user
        :return: Profile of current user
        """

        login_response = self.client.post(self.login_url, self.user_data, format='json')
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(login_response.data.get('token'))}
        follow_response = self.client.post(self.follow_url, **headers)
        self.assertEqual(len(follow_response.data), 13)
        self.assertEqual(follow_response.status_code, status.HTTP_200_OK)

        follow_self_response = self.client.post(
            reverse('profiles:follow', kwargs={"username": self.user_data["username"]}), **headers)
        self.assertIn("You cannot follow yourself", str(follow_self_response.data))

        follow_user_response = self.client.post(reverse('profiles:follow', kwargs={"username": "user5"}), **headers)
        self.assertIn("The user you are looking for does not exist", str(follow_user_response.data))

    def test_unfollow_user(self):
        """
        Ensure user can unfollow another user
        :return: current user follwer
        """
        login_response = self.client.post(self.login_url, self.user_data, format='json')
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(login_response.data.get('token'))}

        unfollow_response = self.client.delete(self.follow_url, **headers)
        self.assertEqual(len(unfollow_response.data), 13)
        self.assertEqual(unfollow_response.status_code, status.HTTP_200_OK)

        unfollow_self_response = self.client.delete(reverse('profiles:follow',
                                                    kwargs={"username": self.user_data["username"]}),
                                                    **headers)

        self.assertIn('You cannot perform that action', str(unfollow_self_response.data))

    def test_following(self):
        """
        Ensure user can get all users he\she is following
        :return: user profiles
        """
        login_response = self.client.post(self.login_url, self.user_data, format='json')
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(login_response.data.get('token'))}
        self.client.post(self.follow_url, **headers)
        following_response = self.client.get(self.following_url, **headers)
        self.assertEqual(len(following_response.data), 1)
        self.assertEqual(following_response.status_code, status.HTTP_200_OK)

    def test_follower(self):
        """
        Ensure user can get all followers
        :return: all followers
        """
        login_response = self.client.post(self.login_url, self.user_data, format='json')
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(login_response.data.get('token'))}
        self.client.post(self.follow_url, **headers)
        follower_response = self.client.get(self.followers_url, **headers)
        self.assertEqual(len(follower_response.data), 1)

    def test_list_authors_profile(self):
        """
        Ensure an authenticated user can view authors profile
        :return: all profiles
        """
        login_response = self.client.post(self.login_url, self.user_data, format='json')
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(login_response.data.get('token'))}
        response = self.client.get(self.profiles_url, **headers)
        self.assertEqual(len(response.data['results']), 1)
