from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Article
from authors.apps.authentication.models import User


class Base(APITestCase):
    def setUp(self):
        """
        We need a logged in user to create an article
        We register a new user and get authorization token for the user.
        """
        self.user_data = {
            "username": "admin",
            "email": "admin@gmail.com",
            "password": "kamila1990",
        }
        self.registration_url = reverse('authentication:register')
        response = self.client.post(self.registration_url, self.user_data,
                                    format='json')
        self.headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(
            response.data['token'])}
        self.article_data = {
            "title": "My Journey to Andela",
            "description": "This article is about how I joined Andela",
            "body": "This is my story to Andela"
        }
        self.article_url = reverse('articles:create')
        self.retrieve_update_delete_url = reverse(
            'articles:retrieveUpdateDelete', kwargs={'pk': 5})

    def tearDown(self):
        self.user_data = None
        self.authorization = None
        self.article_data = None
        self.article_url = None
