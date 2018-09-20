from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Article
from authors.apps.authentication.models import User
from authors.apps.authentication.backends import generate_jwt_token


class Base(APITestCase):
    def setUp(self):
        """
        We need a logged in user who follows an author to receive notifications.
        """
        self.user_one_data = {
            "username": "user",
            "email": "user1@gmail.com",
            "password": "andela2018",
        }
        self.user_two_data = {
            "username": "user2",
            "email": "user2@gmail.com",
            "password": "andela2018",
        }
        self.registration_url = reverse('authentication:register')
        self.login_url = reverse('authentication:login')
        self.article_url = reverse('articles:create')

        register = self.client.post(
            self.registration_url, self.user_one_data, format='json')
        register = self.client.post(
            self.registration_url, self.user_two_data, format='json')

        token_one = generate_jwt_token(self.user_one_data['username'])
        token_two = generate_jwt_token(self.user_two_data['username'])

        activate = self.client.get(
            reverse("authentication:activate_user", args=[token_one]))
        activate = self.client.get(
            reverse("authentication:activate_user", args=[token_two]))
        response_one = self.client.post(
            self.login_url, self.user_one_data, format='json')
        self.headers_one = {
            'HTTP_AUTHORIZATION':
            'Bearer {}'.format(response_one.data['token'])
        }

        response_two = self.client.post(
            self.login_url, self.user_two_data, format='json')
        self.headers_two = {
            'HTTP_AUTHORIZATION':
            'Bearer {}'.format(response_two.data['token'])
        }
        follow = self.client.post(
            reverse(
                'profiles:follow',
                kwargs={"username": self.user_one_data["username"]}),
            **self.headers_two)

        self.article_data = {
            "title": "My Journey to Andela",
            "description": "This article is about how I joined Andela",
            "body": "This is my story to Andela"
        }

    def tearDown(self):
        self.user_data = None
        self.authorization = None
        self.article_data = None
        self.article_url = None
