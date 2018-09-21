from django.urls import reverse
from rest_framework import status

from .base_setup import Base

from authors.apps.authentication.backends import generate_jwt_token
from authors.apps.articles.models import ArticleReport


class ArticleRatingTests(Base):
    def setUp(self):
        """ Set up test environment"""
        super().setUp()

        """
        Register and log in and a new user.
        This user's credentials will used to attempt to update, delete and
        retrieve article reports that aren't their own.
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
        self.non_owner_user_headers = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(
            response.data['token'])}

        """Post an article using the base user's credentials"""
        self.res = self.client.post(self.article_url, self.article_data,
                                    format="json", **self.headers)
        self.slug = self.res.data['slug']

        """Report an article using the base user's credentials"""
        self.res = self.client.post(
            reverse('articles:reportListCreate', kwargs={'slug': self.slug}),
            {'text': 'This article has been plagiarised'},
            format="json", **self.headers)

        self.violate_max_report_attempts_error_message = \
            'You are not allowed to report an article more than five times.'

        self.violate_owner_retrieve_report_error_message = \
            'You are not allowed to view this report.'

        self.violate_owner_update_report_error_message = \
            'You are not allowed to update this report.'

        self.violate_owner_delete_report_error_message = \
            'You are not allowed to delete this report.'

        self.no_reports_message = \
            'No concerns have been raised on this article.'

        self.violate_empty_value_error_message = \
            'Please fill in the rating'

        self.non_existent_article_message = \
            'That article does not exist.'

        self.non_existent_article_report_message = \
            'That article report does not exist.'

    def tearDown(self):
        """ Tear dowm test environment"""
        super().tearDown()

    def test_successful_article_report(self):
        """
        Tests that a user can report a specific article
        """
        report_count = ArticleReport.objects.count()
        response = self.client.post(
            reverse('articles:reportListCreate', kwargs={'slug': self.slug}),
            {'text': 'This article has been plagiarised'},
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ArticleReport.objects.count(), report_count+1)

    def test_successful_article_report_update(self):
        """
        Tests that a user can update the report a specific article
        """
        aricle_report = ArticleReport.objects.first()
        report_count = ArticleReport.objects.count()
        update_response = self.client.put(
            reverse('articles:reportRetrieveUpdateDestroy',
                    kwargs={'slug': self.slug, 'pk': aricle_report.id}),
            {'text': 'This article has been heavily plagiarised'},
            format="json",
            **self.headers)
        self.assertEqual(ArticleReport.objects.count(), report_count)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_successful_article_report_delete(self):
        """
        Tests that a user can delete the report a specific article
        """
        aricle_report = ArticleReport.objects.first()
        report_count = ArticleReport.objects.count()
        update_response = self.client.delete(
            reverse('articles:reportRetrieveUpdateDestroy',
                    kwargs={'slug': self.slug, 'pk': aricle_report.id}),
            format="json",
            **self.headers)
        self.assertEqual(ArticleReport.objects.count(), report_count - 1)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_successful_article_report_retrieve(self):
        """
        Tests that a user can retrieve the report a specific article
        """
        aricle_report = ArticleReport.objects.first()
        update_response = self.client.get(
            reverse('articles:reportRetrieveUpdateDestroy',
                    kwargs={'slug': self.slug, 'pk': aricle_report.id}),
            format="json",
            **self.headers)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_successful_all_article_report_retrieve(self):
        """
        Tests that a user can retrieve all reports of an article
        """
        update_response = self.client.get(
            reverse('articles:reportListCreate',
                    kwargs={'slug': self.slug}),
            format="json",
            **self.headers)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_successful_retrieve_of_non_reported_article(self):
        """
        Tests that a user can retrieve all reports
        """
        # Delete all previous reports
        ArticleReport.objects.all().delete()
        response = self.client.get(
            reverse('articles:reportListCreate',
                    kwargs={'slug': self.slug}),
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         self.no_reports_message)

    def test_unsuccessful_article_report_after_five_article_reports(self):
        """
        Tests if a user can report a specific article after already reporting
        it five times previously
        """
        for x in range(0, 5):
            self.client.post(
                reverse('articles:reportListCreate',
                        kwargs={'slug': self.slug}),
                {'text': 'This article has been plagiarised'},
                format="json",
                **self.non_owner_user_headers)

        response = self.client.post(
            reverse('articles:reportListCreate', kwargs={'slug': self.slug}),
            {'text': 'This article has been plagiarised'},
            format="json",
            **self.non_owner_user_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         self.violate_max_report_attempts_error_message)

    def test_unsuccessful_non_owner_report_retrieve(self):
        """
        Tests if a user can retrieve an article report that doesn't belong to
        them
        """
        aricle_report = ArticleReport.objects.first()
        response = self.client.get(
            reverse('articles:reportRetrieveUpdateDestroy',
                    kwargs={'slug': self.slug, 'pk': aricle_report.id}),
            format="json",
            **self.non_owner_user_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],
                         self.violate_owner_retrieve_report_error_message)

    def test_unsuccessful_non_owner_report_update(self):
        """
        Tests if a user can update an article report that doesn't belong to
        them
        """
        aricle_report = ArticleReport.objects.first()
        response = self.client.put(
            reverse('articles:reportRetrieveUpdateDestroy',
                    kwargs={'slug': self.slug, 'pk': aricle_report.id}),
            {'text': 'This article has been heavily plagiarised'},
            format="json",
            **self.non_owner_user_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],
                         self.violate_owner_update_report_error_message)

    def test_unsuccessful_non_owner_report_delete(self):
        """
        Tests if a user can delete an article report that doesn't belong to
        them
        """
        aricle_report = ArticleReport.objects.first()
        response = self.client.delete(
            reverse('articles:reportRetrieveUpdateDestroy',
                    kwargs={'slug': self.slug, 'pk': aricle_report.id}),
            format="json",
            **self.non_owner_user_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],
                         self.violate_owner_delete_report_error_message)

    def test_unsuccessful_report_of_nonexistent_article(self):
        """
        Tests if a user can report a non existent article
        """
        self.slug = 'fake-slug'
        response = self.client.post(
            reverse('articles:reportListCreate', kwargs={'slug': self.slug}),
            {'text': 'This article has been plagiarised'},
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         self.non_existent_article_message)

    def test_unsuccessful_retrieve_report_of_nonexistent_article(self):
        """
        Tests if a user can retrieve a report of a non existent article
        """
        self.slug = 'fake-slug'
        aricle_report = ArticleReport.objects.first()
        response = self.client.get(
            reverse('articles:reportRetrieveUpdateDestroy',
                    kwargs={'slug': self.slug, 'pk': aricle_report.id}),
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         self.non_existent_article_message)

    def test_unsuccessful_update_report_of_nonexistent_article(self):
        """
        Tests if a user can update a report of a non existent article
        """
        self.slug = 'fake-slug'
        aricle_report = ArticleReport.objects.first()
        response = self.client.put(
            reverse('articles:reportRetrieveUpdateDestroy',
                    kwargs={'slug': self.slug, 'pk': aricle_report.id}),
            {'text': 'This article has been heavily plagiarised'},
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         self.non_existent_article_message)

    def test_unsuccessful_delete_report_of_nonexistent_article(self):
        """
        Tests if a user can delete a report of a non existent article
        """
        self.slug = 'fake-slug'
        aricle_report = ArticleReport.objects.first()
        response = self.client.delete(
            reverse('articles:reportRetrieveUpdateDestroy',
                    kwargs={'slug': self.slug, 'pk': aricle_report.id}),
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         self.non_existent_article_message)

    def test_unsuccessful_retrieve_of_nonexistent_article_report(self):
        """
        Tests if a user can retrieve a non existent article report
        """
        aricle_report = ArticleReport.objects.first()
        response = self.client.get(
            reverse('articles:reportRetrieveUpdateDestroy',
                    kwargs={'slug': self.slug, 'pk': 1000}),
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         self.non_existent_article_report_message)

    def test_unsuccessful_update_of_nonexistent_article_report(self):
        """
        Tests if a user can update a non existent article report
        """
        aricle_report = ArticleReport.objects.first()
        response = self.client.put(
            reverse('articles:reportRetrieveUpdateDestroy',
                    kwargs={'slug': self.slug, 'pk': 1000}),
            {'text': 'This article has been heavily plagiarised'},
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         self.non_existent_article_report_message)

    def test_unsuccessful_delete_of_nonexistent_article_report(self):
        """
        Tests if a user can delete a non existent article report
        """
        aricle_report = ArticleReport.objects.first()
        response = self.client.delete(
            reverse('articles:reportRetrieveUpdateDestroy',
                    kwargs={'slug': self.slug, 'pk': 1000}),
            format="json",
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'],
                         self.non_existent_article_report_message)
