from django.test import TestCase
from django.urls import reverse
from ..models import Article


class Base(TestCase):
    def setUp(self):
        """
        We need a logged in user to create an article
        """
        self.user_data = {
            "username": "user1",
            "email": "user1@user.user",
            "password": "user123user"
        }
        self.registration_url = reverse('authentication:register')
        response = self.client.post(self.registration_url, self.user_data,
                                    format='json')
        self.authorization = {
            'token': response.data['token']
        }
        self.article_data = {
            'title': 'My Journey to Andela',
            'description': 'This article is about how I learnt about Andela,\
            started',
            'body': 'This is my story to Andela'
        }
        self.article_url = reverse('article:create')

    def tearDown(self):
        self.user_data = None
        self.authorization = None
        self.article_data = None
        self.article_url = None
