from .base_setup import Base
from rest_framework import status
from django.urls import reverse


class ArticleTests(Base):
    def setUp(self):
        super().setUp()
        self.client.post(self.article_url, self.article_data,
                         format="json", **self.headers)

    def tearDown(self):
        super().tearDown()

    def test_retrieve_all_articles(self):
        """
        Tests that a client can retrieve all articles
        """
        response = self.client.get(
            self.article_url, format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_can_retrieve_a_single_article(self):
        """
        Tests that a client can retrieve a single article
        """
        response = self.client.get(
            reverse(
                'articles:retrieveUpdateDelete', kwargs={'pk': 2}), format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['id'] == 2)

    def test_cannot_retrieve_a_non_existing_article(self):
        """
        Tests that a client cannot retrieve an article which does not exist
        """
        response = self.client.get(
            reverse(
                'articles:retrieveUpdateDelete', kwargs={'pk': -1}),
            format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)