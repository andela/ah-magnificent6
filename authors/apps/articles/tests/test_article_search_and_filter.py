from .base_setup import Base
from rest_framework import status
from django.urls import reverse


class SearchFilterTests(Base):
    def setUp(self):
        super().setUp()
        tags = ["Andela","Test"]
        for tag in tags:
            self.article_data["tags"]=tag
            self.client.post(self.article_url, self.article_data,
                         format="json", **self.headers)

    def tearDown(self):
        super().tearDown()

    def test_search_success(self):
        """ Test successful search """
        # Search using the name test which is in one tag
        search = "test"
        response = self.client.get(
            self.article_url+'?article_tags__tag__icontains={}'.format(search), format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        # Make the strings lowercase as the search is not case sensitive
        self.assertEqual(str.lower(response.data['results'][0]['article_tags'][0]),str.lower(search))
    
    def test_search_no_result(self):
        """ Test no article found from search """
        # Search using the string "nothing" which is not in tags, authors or the title
        search = "nothing"
        response = self.client.get(
            self.article_url+'?article_tags__tag__icontains={}'.format(search), format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_filter_by_author(self):
        """ Filter artiles only by author """
        # Filter articles by author
        author=self.user_data['username']
        response = self.client.get(
            self.article_url+'?author___username__icontains={}'.format(author), format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_author_and_title(self):
        """ Filter by author and title """
        author = self.user_data['username']
        title = self.article_data['title'] 
        response = self.client.get(
            self.article_url+'?author___username__icontains={}&?title__icontains={}'
            .format(author, title), format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_by_author_title_and_tags(self):
        """ Filter by author, title and tag.
            Only one article has the tag "test"
        """
        author = self.user_data['username']
        title = self.article_data['title']
        tag = "test"
        response = self.client.get(
            self.article_url+'?author___username__icontains={}&title__icontains={}&article_tags__tag__icontains={}'
            .format(author, title, tag), format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(str.lower(response.data['results'][0]['article_tags'][0]),str.lower(tag))
