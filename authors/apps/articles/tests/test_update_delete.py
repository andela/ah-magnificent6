from .base_setup import Base
from rest_framework import status
from django.urls import reverse


class ArticleDeleteUpdateTests(Base):
    def setUp(self):
        super().setUp()
        self.client.post(self.article_url, self.article_data,
                         format="json", **self.headers)
        self.retrieve_update_delete_url = reverse(
            'articles:retrieveUpdateDelete', kwargs={'pk': 4})

    def tearDown(self):
        super().tearDown()

    def test_can_delete_an_article(self):
        """
        Tests that a client can delete a specific article
        """
        response = self.client.delete(
            reverse(
                'articles:retrieveUpdateDelete', kwargs={'pk': 5}),
            format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_delete_other_users_articles(self):
        """
        Tests that a user cannot delete article they do not own
        """
        # Log in/ register a new user and use this user's credentials to
        # delete article belonging to the other user
        user_data = {
            "username": "new_user",
            "email": "user@gmail.com",
            "password": "kamila1990",
        }
        response = self.client.post(self.registration_url, user_data,
                                    format='json')
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(
            response.data['token'])}
        self.client.post(self.article_url, self.article_data,
                         format="json", **headers)
        response = self.client.delete(
            reverse(
                'articles:retrieveUpdateDelete', kwargs={'pk': 8}),
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_edit_an_article(self):
        """
        Tests that a client can update details of an article
        """
        response = self.client.put(
            reverse(
                'articles:retrieveUpdateDelete', kwargs={'pk': 6}),
            data=self.article_data,
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], self.article_data['body'])
