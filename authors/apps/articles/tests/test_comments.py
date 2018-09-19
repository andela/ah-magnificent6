from .base_setup import Base
from rest_framework import status
from django.urls import reverse
from authors.apps.authentication.backends import generate_jwt_token


class CommentTest(Base):
    def setUp(self):
        """ Setup data for the tests """
        self.user_data = {
            "username": "John",
            "email": "john@company.com",
            "password": "john1234"
        }
        self.article_data = {
            "title": "My Journey to Andela",
            "description": "This article is about how I joined Andela",
            "body": "This is my story to Andela"
        }
        self.article_data2 = {
            "title": "My Journey currently in Andela",
            "description": "This article is about how I am currently in Andela",
            "body": "This is my story to Andela"
        }
        self.registration_url = reverse('authentication:register')
        self.login_url = reverse('authentication:login')

        self.article_url = reverse('articles:create')
        self.register_user = self.client.post(self.registration_url, self.user_data)
        token = generate_jwt_token(self.user_data['username'])
        self.client.get(reverse("authentication:activate_user", args=[token]))
        login_response = self.client.post(self.login_url, self.user_data, format='json')
        self.headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(login_response.data.get('token'))}
        self.slug = self.client.post(self.article_url, self.article_data, format="json", **self.headers)
        self.comments_url = reverse('articles:comments', kwargs={"slug": self.slug.data['slug']})

    def test_get_comments(self):
        """Test a user can get all comments"""

        list_comment_response = self.client.get(self.comments_url,
                                                self.article_data, format='json',
                                                **self.headers)
        self.assertEqual(list_comment_response.status_code, status.HTTP_200_OK)

    def test_create_comment(self):
        create_comment_response = self.client.post(self.comments_url,
                                                   {"comment": "Amazing", 'article_id': 1},
                                                   format='json', **self.headers)
        print(create_comment_response.data)


