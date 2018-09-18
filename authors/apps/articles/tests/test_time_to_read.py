from .base_setup import Base
from rest_framework import status
from django.urls import reverse


class ArticleReadTime(Base):
    def setUp(self):
        super().setUp()
        response = self.client.get(
            self.article_url, format="json", **self.headers)
        self.initial_count = len(response.data["results"])
        response = self.client.post(self.article_url, self.article_data,
                                    format="json", **self.headers)
        self.article_slug = response.data['slug']
        self.time_to_read = '1 min'
        self.retrieve_update_delete_url = reverse(
            'articles:retrieveUpdateDelete', kwargs={'slug': self.article_slug})

    def test_can_retrieve_article_with_read_time(self):
        """
        Tests that a client can retrieve an article with the read time 
        """
        response = self.client.get(self.retrieve_update_delete_url,
                                   format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['time_to_read'] == self.time_to_read)
