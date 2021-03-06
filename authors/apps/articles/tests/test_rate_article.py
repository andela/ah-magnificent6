from django.urls import reverse
from rest_framework import status

from .base_setup import Base

from authors.apps.authentication.backends import generate_jwt_token
from authors.apps.articles.models import ArticleRating


class ArticleRatingTests(Base):
    def setUp(self):
        """ Set up test environment"""
        super().setUp()

        """
        Log in and register a new user.
        Use this user's credentials to create an article. We will perform our
        tests on this created article using the user set up in our base test.
        """
        user_data = {
            "username": "new_user",
            "email": "user@gmail.com",
            "password": "kamila1990",
        }
        """Register user"""
        self.client.post(self.registration_url, user_data,
                         format='json')
        token = generate_jwt_token(user_data['username'])

        self.client.get(
            reverse("authentication:activate_user", args=[token]))

        """Login the user"""
        response = self.client.post(self.login_url, user_data,
                                    format='json')
        self.author_headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(
            response.data['token'])}

        """Post an article"""
        self.res = self.client.post(self.article_url, self.article_data,
                                    format="json", **self.author_headers)

        self.slug = self.res.data['slug']

        self.violate_max_value_error_message = \
            'Ensure this value is less than or equal to 5.'

        self.violate_min_value_error_message = \
            'Ensure this value is greater than or equal to 1.'

        self.violate_empty_value_error_message = \
            'Please fill in the rating'

        self.non_existent_article_message = \
            'That article does not exist'

        self.rate_own_article_error_message = \
            'Sorry, but you cannot rate your own article.'

    def tearDown(self):
        """ Tear dowm test environment"""
        super().tearDown()

    def test_successful_article_rate(self):
        """
        Tests that a user can rate a specific article
        """
        ratings_count = ArticleRating.objects.count()
        response = self.client.post(
            reverse('articles:rate', kwargs={'slug': self.slug}),
            {'rating': 4},
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ArticleRating.objects.count(), ratings_count+1)

    def test_successful_article_rate_update(self):
        """
        Tests that a user can update the rating a specific article
        """

        self.client.post(
            reverse('articles:rate', kwargs={'slug': self.slug}),
            {'rating': 4},
            format="json",
            **self.headers)

        ratings_count = ArticleRating.objects.count()
        update_response = self.client.post(
            reverse('articles:rate', kwargs={'slug': self.slug}),
            {'rating': 5},
            format="json",
            **self.headers)
        self.assertEqual(update_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ArticleRating.objects.count(), ratings_count)

    def test_unsuccessful_rating_with_negative_rate_value(self):
        """
        Tests if a user can rate a specific article with a negative value
        """
        response = self.client.post(
            reverse('articles:rate', kwargs={'slug': self.slug}),
            {'rating': -4},
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['errors']['rating'][0]),
                         self.violate_min_value_error_message)

    def test_unsuccessful_rating_with_rate_value_more_than_five(self):
        """
        Tests if a user can rate a specific article with a value more than 5
        """
        response = self.client.post(
            reverse('articles:rate', kwargs={'slug': self.slug}),
            {'rating': 6},
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['errors']['rating'][0]),
                         self.violate_max_value_error_message)

    def test_unsuccessful_rating_with_empty_rate_value(self):
        """
        Tests if a user can rate a specific article with an empty value
        """
        response = self.client.post(
            reverse('articles:rate', kwargs={'slug': self.slug}),
            {'rating': None},
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['errors']['rating'][0]),
                         self.violate_empty_value_error_message)

    def test_unsuccessful_rating_of_nonexistent_article(self):
        """
        Tests if a user can rate a non existent article
        """
        self.slug = 'fake-slug'
        response = self.client.post(
            reverse('articles:rate', kwargs={'slug': self.slug}),
            {'rating': None},
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         self.non_existent_article_message)

    def test_unsuccessful_rating_of_own_article(self):
        """
        Tests if a user can rate a their own article
        """
        response = self.client.post(
            reverse('articles:rate', kwargs={'slug': self.slug}),
            {'rating': None},
            format="json",
            **self.author_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(self.rate_own_article_error_message,
                      response.data['message'])
