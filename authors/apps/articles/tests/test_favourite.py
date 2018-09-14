from .base_setup import Base
from rest_framework import status
from django.urls import reverse


class ArticleDeleteUpdateTests(Base):
    """Test suite for favouriting articles."""

    def setUp(self):
        """Setup data for the tests."""
        super().setUp()
        self.res = self.client.post(
            self.article_url, self.article_data, format="json", **self.headers)

    def tearDown(self):
        """Teardown for the tests."""
        super().tearDown()

    def test_favourite_article(self):
        """
        Tests that a user can favorite an article.
        """
        slug = self.res.data['slug']
        response = self.client.post(
            reverse('articles:favourite_article', kwargs={'slug': slug}),
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_favourite_article(self):
        """
        Tests that a user can unfavorite an article.
        """
        slug = self.res.data['slug']
        favourite = self.client.post(
            reverse('articles:favourite_article', kwargs={'slug': slug}),
            format="json",
            **self.headers)
        unfavourite = self.client.post(
            reverse('articles:favourite_article', kwargs={'slug': slug}),
            format="json",
            **self.headers)
        self.assertEqual(unfavourite.status_code, status.HTTP_200_OK)

    def test_favourite_non_existing_article(self):
        """
        Tests that a user unsuccessfully favouriting non-existing article.
        """
        slug = self.res.data['slug'] + "KDKDJC"
        favourite = self.client.post(
            reverse('articles:favourite_article', kwargs={'slug': slug}),
            format="json",
            **self.headers)
        unfavourite = self.client.post(
            reverse('articles:favourite_article', kwargs={'slug': slug}),
            format="json",
            **self.headers)
        self.assertEqual(unfavourite.status_code, status.HTTP_404_NOT_FOUND)
