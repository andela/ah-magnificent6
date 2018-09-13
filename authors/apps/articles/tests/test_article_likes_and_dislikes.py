from rest_framework import status
from django.urls import reverse
from .base_setup import Base


class ArticleLikeTests(Base):
    def setUp(self):
        super().setUp()
        response = self.client.post(self.article_url, self.article_data,
                                    format="json", **self.headers)
        self.article_slug = response.data['slug']
        self.likes_dislikes_url = reverse(
            'articles:likeArticles', kwargs={'slug': self.article_slug})
        self.like = {'like': True}
        self.dislike = {'like': False}
        self.non_existing_slug = 'mndbfkjhifhilw'

    def tearDown(self):
        super().tearDown()

    def test_can_like_an_article(self):
        """
        Tests that a user can like an article
        """
        response = self.client.post(self.likes_dislikes_url,
                                    data=self.like,
                                    format="json",
                                    **self.headers
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_like_an_article_more_than_once(self):
        """
        Tests that a user cannot like/dislike an article more than once
        """
        res = self.client.post(self.likes_dislikes_url,
                               format="json",
                               data=self.like,
                               **self.headers
                               )
        print(res.data)
        response = self.client.post(self.likes_dislikes_url,
                                    format="json",
                                    data=self.like,
                                    **self.headers
                                    )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_like_non_existing_article(self):
        """
        Tests that a user cannot like an article which does not exist
        """
        response = self.client.post(
            reverse('articles:likeArticles', kwargs={
                    'slug': self.non_existing_slug}),
            format="json",
            data=self.like,
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_dislike_an_article(self):
        """
        Tests that a user can dislike an article
        """
        response = self.client.post(self.likes_dislikes_url,
                                    data=self.dislike,
                                    format="json",
                                    **self.headers
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_like_an_article_without_sending_necessary_payload(self):
        """
        Tests that a user cannot dislike an article without specifying
        his/her intention
        """
        response = self.client.post(self.likes_dislikes_url,
                                    format="json",
                                    **self.headers
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_user_change_a_like_to_a_dislike(self):
    #     """
    #     Tests that a user who likes an article but changes mind to dislike it
    #     can do so.
    #     """
    #     self.client.post(self.likes_dislikes_url,
    #                      format="json",
    #                      data=self.like,
    #                      **self.headers
    #                      )
    #     response = self.client.post(self.likes_dislikes_url,
    #                                 format="json",
    #                                 data=self.dislike,
    #                                 **self.headers
    #                                 )
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_user_change_a_dislike_to_a_like(self):
    #     """
    #     Tests that a user who dislikes an article but changes mind to like it
    #     can do so.
    #     """
    #     self.client.post(self.likes_dislikes_url,
    #                      format="json",
    #                      data=self.dislike,
    #                      **self.headers)
    #     response = self.client.post(self.likes_dislikes_url,
    #                                 format="json",
    #                                 data=self.like,
    #                                 **self.headers
    #                                 )
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
