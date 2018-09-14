from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

class SocialAuthentication(APITestCase):
    def setUp(self):
        """ Setup data for tests """
        self.oauth_url = reverse('authentication:social_auth')
        self.client = APIClient()
        self.access_token_oauth2 = "EAAKBM4Ifwb8BAIJkV2yin7AAF2ZA5ZBJzUHLHOIM84FyYVODyZBfiGPXTNMFe4ljFxZABVAvQMbFStM2jixTGRmWUyYXfCSQwsu2jJmNM0QO33cC0W4IGMnZARGdc1DA6mYqodyRZAewhYFs5dSFQi4yQdBOjlTJnY8C48BFQ3ZB6WtUGNHvISPysqP6ZASdLRMqwi7eMKa3DnrZBhylteeConby21elnpuPR4OGFWRRVfwZDZD"
        self.access_token_oauth1 = "915919767135035399-xGVkH4T3kmNdIhm3WXGmJkaN11yOvuN"
        self.access_token_secret_oauth1 = "bCwPum2FRI28nAvxXxCLXEj4vMngz5wHg8R5Jl1ug7D7t"

    
    def test_successfull_social_login(self):
        """ Tests for suiccessfull login using . Twitter keys do not expire """
        data = {
            "provider":"twitter",
            "access_token":self.access_token_oauth1,
            "access_token_secret":self.access_token_secret_oauth1
            }
        response = self.client.post(self.oauth_url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        self.assertTrue(response.data["token"])

    
    def test_missing_provider(self):
        """ Test for missing provider """
        data = {"access_token":self.access_token_oauth2}
        response = self.client.post(self.oauth_url, data=data)

        self.assertEqual(response.status_code, 400)
    
    def test_missing_access_token(self):
        """ Test for missing access token in json request """
        data = {"provider":"facebook"}
        response = self.client.post(self.oauth_url, data=data)

        self.assertEqual(response.status_code, 400)

    def test_invalid_token(self):
        """ Test expired or faulty token """
        data = {
            "access_token":"invalidtoken",
            "provider":"facebook"
        }
        response = self.client.post(self.oauth_url, data=data)

        self.assertEqual(response.status_code, 400)
    
    def test_invalid_provider(self):
        """ Test response of invalid provider """
        data = {
            "access_token":self.access_token_oauth2,
            "provider":"facebookImbo"
        }
        response = self.client.post(self.oauth_url, data=data)

        self.assertEqual(response.status_code, 400)

    def test_missing_access_token_secret(self):
        """ Test OAuth1 access token secret. Twitter uses OAuth1 """
        data = {
            "provider":"twitter",
            "access_token":self.access_token_oauth1
        }
        response = self.client.post(self.oauth_url, data=data)
        self.assertEqual(response.status_code, 400)



