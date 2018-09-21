from .base_setup import Base
from rest_framework import status
from django.urls import reverse


class ArticleTests(Base):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_create_article(self):
        """
        Tests that a user can create a new article
        """
        response = self.client.post(self.article_url,
                                    self.article_data,
                                    format="json",
                                    **self.headers
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.article_data['title'])

    def test_create_article_with_tags(self):
        """
        Tests that a user can tag their articles when creating them
        """
        # add tags to the article data
        self.article_data['tags'] = 'Learning,Reading,Software'
        response = self.client.post(self.article_url,
                                    self.article_data,
                                    format="json",
                                    **self.headers
                                    )
        slug = response.data['slug']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.retrieve_update_delete_url = reverse(
            'articles:retrieveUpdateDelete', kwargs={'slug': slug})
        response = self.client.get(self.retrieve_update_delete_url,
                                   format="json", **self.headers)
        self.assertTrue(len(response.data['article_tags']) > 0)

    def test_create_article_with_tags_already_in_database(self):
        """
        Tests that a user can create several articles with the same tags.
        """
        # add tags to the article data
        self.article_data['tags'] = 'Learning,Reading,Software'
        self.client.post(self.article_url,
                         self.article_data,
                         format="json",
                         **self.headers
                         )
        response = self.client.post(self.article_url,
                                    self.article_data,
                                    format="json",
                                    **self.headers
                                    )
        slug = response.data['slug']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.retrieve_update_delete_url = reverse(
            'articles:retrieveUpdateDelete', kwargs={'slug': slug})
        response = self.client.get(self.retrieve_update_delete_url,
                                   format="json", **self.headers)
        self.assertTrue(len(response.data['article_tags']) > 0)

    def test_cannot_create_article_with_missing_a_title(self):
        """
        Tests that a user cannot create a new article without a title
        """
        self.article_data['title'] = None
        response = self.client.post(self.article_url,
                                    self.article_data,
                                    format='json',
                                    **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_article_with_missing_a_body(self):
        """
        Tests a that user cannot create a new article without a body
        """
        self.article_data['body'] = None
        response = self.client.post(self.article_url,
                                    self.article_data,
                                    format='json',
                                    **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_article_with_missing_a_description(self):
        """
        Tests a that user cannot create a new article without a description
        """
        self.article_data['description'] = None
        response = self.client.post(self.article_url,
                                    self.article_data,
                                    format='json',
                                    **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
