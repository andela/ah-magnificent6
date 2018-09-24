from rest_framework import status
from django.urls import reverse
from .base_setup import Base
from authors.apps.authentication.backends import generate_jwt_token


class ArticleBookmarkTests(Base):
    def setUp(self):
        super().setUp()
        response = self.client.post(self.article_url, self.article_data,
                                    format="json", **self.headers)
        self.article_slug = response.data['slug']
        self.article_bookmark_url = reverse(
            'articles:bookmark_article', kwargs={'slug': self.article_slug})
        self.non_existing_slug = 'mndbfkjhifhilw'
        self.article_bookmark_retrieval_url = reverse(
            'articles:user_bookmarks', kwargs={'pk': 0}
        )

    def tearDown(self):
        super().tearDown()

    def test_can_bookmark_an_article(self):
        """
        Tests that a user can bookmark an article
        """
        response = self.client.post(self.article_bookmark_url,
                                    format="json",
                                    **self.headers
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_using_get_method_on_end_point_for_bookmarking_article_fails(self):

        response = self.client.get(self.article_bookmark_url,
                                   format="json",
                                   **self.headers
                                   )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_bookmark_an_article_more_than_once(self):
        """
        Tests that a user can bookmark an article more than once
        """
        self.client.post(self.article_bookmark_url,
                         format="json",
                         **self.headers
                         )
        response = self.client.post(self.article_bookmark_url,
                                    format="json",
                                    **self.headers
                                    )
        self.assertTrue(response.data['errors'])

    def test_cannot_bookmark_a_non_existing_article(self):
        """
        Tests that a user cannot bookmark a non existing article
        """
        self.article_bookmark_url = reverse(
            'articles:bookmark_article', kwargs={'slug': self.non_existing_slug})
        response = self.client.post(self.article_bookmark_url,
                                    format="json",
                                    **self.headers
                                    )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_retrieve_all_bookmarks(self):
        """
        Tests that a user can retrieve bookmarks
        """
        self.client.post(self.article_bookmark_url,
                         format="json",
                         **self.headers
                         )
        article_bookmark_retrieval_url = reverse(
            'articles:user_bookmarks')
        response = self.client.get(article_bookmark_retrieval_url,
                                   format="json",
                                   **self.headers
                                   )
        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve_a_single_bookmark(self):
        """
        Tests that a user can retrieve a single bookmark
        """
        response = self.client.post(self.article_bookmark_url,
                                    format="json",
                                    **self.headers
                                    )
        bookmark_id = response.data['id']
        article_bookmark_retrieval_url = reverse(
            'articles:user_bookmarks', kwargs={'pk': bookmark_id})
        response = self.client.get(article_bookmark_retrieval_url,
                                   format="json",
                                   **self.headers
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_all_bookmarks(self):
        """
        Tests that a user can delete all bookmarks at once
        """
        response = self.client.post(self.article_bookmark_url,
                                    format="json",
                                    **self.headers
                                    )
        article_bookmark_retrieval_url = reverse(
            'articles:user_bookmarks')
        response = self.client.delete(article_bookmark_retrieval_url,
                                      format="json",
                                      **self.headers
                                      )
        self.assertEqual(response.data['message'],
                         'All bookmarks deleted successfully')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_a_bookmark(self):
        """
        Tests that a user can delete a bookmark
        """
        response = self.client.post(self.article_bookmark_url,
                                    format="json",
                                    **self.headers
                                    )
        bookmark_id = response.data['id']
        article_bookmark_retrieval_url = reverse(
            'articles:user_bookmarks', kwargs={'pk': bookmark_id})
        response = self.client.delete(article_bookmark_retrieval_url,
                                      format="json",
                                      **self.headers
                                      )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_delete_non_existing_bookmark(self):
        """
        Tests that a user cannot delete non existing bookmarks
        """
        a = -1
        article_bookmark_retrieval_url = reverse(
            'articles:user_bookmarks', kwargs={'pk': a})
        response = self.client.delete(article_bookmark_retrieval_url,
                                      format="json",
                                      **self.headers
                                      )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_delete_other_users_bookmarks(self):
        """
        Tests that a user cannot delete a bookmark they do not own
        """
        # Log in/ register a new user and use this user's credentials to
        # delete bookmark belonging to the other user
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
        response = self.client.post(self.article_bookmark_url,
                                    format="json",
                                    **self.headers
                                    )
        bookmark_id = response.data['id']
        article_bookmark_retrieval_url = reverse(
            'articles:user_bookmarks', kwargs={'pk': bookmark_id})
        response = self.client.delete(article_bookmark_retrieval_url,
                                      format="json",
                                      **headers
                                      )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
