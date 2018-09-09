from .base_setup import Base
from rest_framework import status
from django.urls import reverse


class ArticleTests(Base):
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
        response = self.client.get(
            self.article_url, format="json", **self.headers)
        print(response.data)
        response = self.client.delete(
            self.retrieve_update_delete_url, format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
