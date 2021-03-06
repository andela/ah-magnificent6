from .base_setup import Base
from rest_framework import status
from django.urls import reverse
from authors.apps.authentication.backends import generate_jwt_token


class ArticleDeleteUpdateTests(Base):
    def setUp(self):
        super().setUp()

        response = self.client.post(
            self.article_url, self.article_data, format="json", **self.headers)
        self.article_slug = response.data['slug']
        self.retrieve_update_delete_url = reverse(
            'articles:retrieveUpdateDelete', kwargs={'slug': self.article_slug})
        self.non_existing_article_url = reverse(
            'articles:retrieveUpdateDelete', kwargs={'slug': 'afbkjhlhlih'})

    def tearDown(self):
        super().tearDown()

    def test_can_delete_an_article(self):
        """
        Tests that a client can delete a specific article
        """
        response = self.client.delete(
            self.retrieve_update_delete_url, format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_delete_a_non_existing_article(self):
        """
        Tests that a client cannot delete an article which does not exist
        """
        response = self.client.delete(
            self.non_existing_article_url,
            format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
        user_register = self.client.post(
            self.registration_url, user_data, format='json')
        token = generate_jwt_token(user_data['username'])
        activate = self.client.get(
            reverse("authentication:activate_user", args=[token]))
        response = self.client.post(self.login_url, user_data, format='json')
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(response.data['token'])
        }
        self.client.post(
            self.article_url, self.article_data, format="json", **headers)
        response = self.client.delete(
            self.retrieve_update_delete_url, format="json", **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_edit_an_article(self):
        """
        Tests that a client can update details of an article
        """
        response = self.client.put(
            self.retrieve_update_delete_url,
            data=self.article_data,
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], self.article_data['body'])

    def test_can_add_tags_to_an_article(self):
        """
        Tests that a client can add tags to an article on updating
        """
        self.article_data['tags'] = 'Learning,Reading,Software'
        response = self.client.put(
            self.retrieve_update_delete_url,
            data=self.article_data,
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['article_tags']) == 3)

    def test_can_remove_tags_to_an_article(self):
        """
        Tests that a client can add tags to an article on updating
        """
        self.article_data['tags'] = 'Learning,Reading,Software'
        response = self.client.post(self.article_url,
                                    self.article_data,
                                    format="json",
                                    **self.headers
                                    )
        slug = response.data['slug']
        self.retrieve_update_delete_url = reverse(
            'articles:retrieveUpdateDelete', kwargs={'slug': slug})
        # remove tags for article data
        self.article_data['tags'] = None
        response = self.client.put(
            self.retrieve_update_delete_url,
            data=self.article_data,
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['article_tags']) == 0)

    def test_cannot_edit_non_existing_article(self):
        """
        Tests that a client cannot update details of an article which does
        not exist
        """
        response = self.client.put(self.non_existing_article_url,
                                   data=self.article_data,
                                   format="json",
                                   **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_edit_other_users_articles(self):
        """
        Tests that a user cannot edit article they do not own
        """
        # Log in/ register a new user and use this user's credentials to
        # edit article belonging to the other user
        user_data = {
            "username": "new_user",
            "email": "user@gmail.com",
            "password": "kamila1990",
        }
        user_register = self.client.post(self.registration_url, user_data,
                                         format='json')
        token = generate_jwt_token(user_data['username'])
        activate = self.client.get(
            reverse("authentication:activate_user", args=[token]))
        response = self.client.post(self.login_url, user_data,
                                    format='json')
        headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(
            response.data['token'])}
        self.client.post(self.article_url, self.article_data,
                         format="json", **headers)
        response = self.client.put(self.retrieve_update_delete_url,
                                   format="json",
                                   **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
