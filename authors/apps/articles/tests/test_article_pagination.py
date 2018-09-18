from .base_setup import Base
from rest_framework import status
from django.urls import reverse

# import settings to overide page size
from authors.settings import REST_FRAMEWORK

# Override your changes.
REST_FRAMEWORK['PAGE_SIZE'] = 2


class PaginationTests(Base):
    def setUp(self):
        super().setUp()
        self.client.post(self.article_url, self.article_data,
                         format="json", **self.headers)

    def tearDown(self):
        super().tearDown()

    def test_pagination(self):
        """ Test successful pagination """
        # First create multiple articles
        i = 0
        while i < 4:
            # Create 5 articles
            self.client.post(self.article_url, self.article_data,
                             format="json", **self.headers)
            i += 1

        response = self.client.get(
            self.article_url+'?page=1', format="json", **self.headers)
        next_url = "http://testserver{}?page=2".format(self.article_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['next'], next_url)

    def test_no_second_page(self):
        """ Test for no second page """
        response = self.client.get(
            self.article_url+'?page=2', format="json", **self.headers)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_next_page(self):
        """ Test for no next page """
        response = self.client.get(
            self.article_url+'?page=1', format="json", **self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['next'], None)
