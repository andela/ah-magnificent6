""" module to test registration. """
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authors.apps.authentication.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        """ Setup data for the tests """
        self.valid_user = {
            "username": "user1",
            "email": "user1@user.user",
            "password": "user123user"
        }
        self.registration_url = reverse('authentication:register')
        self.succesfull_register_message = 'Welcome, you have successfully registered to Author\'s Haven!'
        self.violate_unique_email_message = 'That email is already used. Sign in instead or try another'
        self.violate_unique_username_message = 'That username is taken. Please try another'
        self.violate_password_pattern_message = 'Invalid password. Please choose a password with at least a letter and a number.'
        self.empty_email_error_message = b'{"errors":{"email":["Please fill in the email"]}}'
        self.empty_username_error_message = b'{"errors":{"username":["Please fill in the username"]}}'
        self.empty_password_error_message = b'{"errors":{"password":["Please fill in the password"]}}'

    def test_successful_registered_user(self):
        """ Test that a user is successfully registered. """
        users = User.objects.count()
        response = self.client.post(self.registration_url,
                                    self.valid_user, format='json')
        self.assertEqual(response.data['email'],
                         self.valid_user['email'])
        self.assertEqual(response.data['username'],
                         self.valid_user['username'])
        self.assertEqual(User.objects.count(), (users+1))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(response.data['token'])
        self.assertEqual(response.data['message'],
                         self.succesfull_register_message)

    def test_unsuccessful_register_existing_user(self):
        """ Test that one cannot register twice with same credentials """
        self.client.post(self.registration_url, self.valid_user, format='json')
        response = self.client.post(
            self.registration_url, self.valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['email'][0],
                         self.violate_unique_email_message)
        self.assertEqual(response.data['errors']['username'][0],
                         self.violate_unique_username_message)

    def test_unsuccessful_register_without_username(self):
        """ Test user cannot register without a username. """
        del self.valid_user['username']
        response = self.client.post(
            self.registration_url, self.valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_register_empty_username(self):
        """ Test that a user cannot register empty string. """
        self.valid_user['username'] = " "
        response = self.client.post(
            self.registration_url, self.valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_register_with_email_wrong_format(self):
        """ Test that the user enters an email in the correct format """
        self.valid_user['email'] = "wrongformatemail"
        response = self.client.post(
            self.registration_url, self.valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_registration_empty_email(self):
        """ Test that the user does not enter an empty email """
        self.valid_user['email'] = " "
        response = self.client.post(
            self.registration_url, self.valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_registration_with_weak_password(self):
        """ Test that a user enters a weak password with less characters """
        self.valid_user['password'] = "1234"
        response = self.client.post(
            self.registration_url, self.valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_registration_without_password(self):
        """ Test that a user enters no password """
        del self.valid_user['password']
        response = self.client.post(
            self.registration_url, self.valid_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsuccessful_registration_with_all_numeric_password(self):
        """ Test that a user enters a password with numbers only """
        self.valid_user['password'] = "123409275"
        response = self.client.post(
            self.registration_url, self.valid_user, format='json')
        self.assertEqual(response.data['errors']['error'][0],
                         self.violate_password_pattern_message)

    def test_unsuccessful_registration_with_all_letter_password(self):
        """ Test that a user enters a password with numbers only """
        self.valid_user['password'] = "ABDCefgtd"
        response = self.client.post(
            self.registration_url, self.valid_user, format='json')
        self.assertEqual(response.data['errors']['error'][0],
                         self.violate_password_pattern_message)

    def test_unsuccessful_registration_with_empty_email(self):
        """ Test that a user enters empty values for email """
        self.valid_user['email'] = ""
        response = self.client.post(
            self.registration_url, self.valid_user, format='json')
        self.assertEqual(response.content,
                         self.empty_email_error_message)

    def test_unsuccessful_registration_with_empty_username(self):
        """ Test that a user enters empty values for username """
        self.valid_user['username'] = ""
        response = self.client.post(
            self.registration_url, self.valid_user, format='json')
        self.assertEqual(response.content,
                         self.empty_username_error_message)

    def test_unsuccessful_registration_with_empty_password(self):
        """ Test that a user enters empty values for password """
        self.valid_user['password'] = ""
        response = self.client.post(
            self.registration_url, self.valid_user, format='json')
        self.assertEqual(response.content,
                         self.empty_password_error_message)
