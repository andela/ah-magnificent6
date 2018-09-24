from rest_framework import status
from django.urls import reverse
from .base_setup import Base


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

    def test_user_can_retrieve_bookmarks(self):
        """
        Tests that a user can retrieve bookmarks
        """
        response = self.client.get(self.article_bookmark_retrieval_url,
                                   format="json",
                                   **self.headers
                                   )
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
        response = self.client.get(article_bookmark_retrieval_url,
                                   format="json",
                                   **self.headers
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_delete_non_existing_bookmark(self):
        """
        Tests that a user cannot delete non existing bookmarks
        """
        a = '-1'
        article_bookmark_retrieval_url = reverse(
            'articles:user_bookmarks', kwargs={'pk': a})
        print(article_bookmark_retrieval_url)
        response = self.client.get(article_bookmark_retrieval_url,
                                   format="json",
                                   **self.headers
                                   )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
