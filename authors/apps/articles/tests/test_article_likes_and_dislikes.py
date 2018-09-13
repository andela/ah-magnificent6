from rest_framework import status
from django.urls import reverse
from .base_setup import Base


class ArticleTests(Base):
    def setUp(self):
        super().setUp()
        self.client.post(self.article_url, self.article_data,
                         format="json", **self.headers)
        self.like = {'like': True}
        self.dislike = {'like': False}

    def tearDown(self):
        super().tearDown()

    def test_can_like_an_article(self):
        """
        Tests that a user can like an article
        """
        response = self.client.post(
            reverse('articles:likeArticles', kwargs={'pk': 2}),
            data=self.like,
            format="json",
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_like_an_article_more_than_once(self):
        """
        Tests that a user cannot like/dislike an article more than once
        """
        self.client.post(
            reverse('articles:likeArticles', kwargs={'pk': 4}),
            format="json",
            data=self.like,
            **self.headers
        )
        response = self.client.post(
            reverse('articles:likeArticles', kwargs={'pk': 4}),
            format="json",
            data=self.like,
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_like_non_existing_article(self):
        """
        Tests that a user cannot like an article which does not exist
        """
        response = self.client.post(
            reverse('articles:likeArticles', kwargs={'pk': -1}),
            format="json",
            data=self.like,
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_dislike_an_article(self):
        """
        Tests that a user can dislike an article
        """
        response = self.client.post(
            reverse('articles:likeArticles', kwargs={'pk': 1}),
            data=self.dislike,
            format="json",
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_dislike_an_article_without_sending_necessary_payload(self):
        """
        Tests that a user cannot dislike an article without specifying
        his/her intention
        """
        response = self.client.post(
            reverse('articles:likeArticles', kwargs={'pk': 1}),
            format="json",
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_like_an_article_without_sending_necessary_payload(self):
        """
        Tests that a user cannot dislike an article without specifying
        his/her intention
        """
        response = self.client.post(
            reverse('articles:likeArticles', kwargs={'pk': 1}),
            format="json",
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
