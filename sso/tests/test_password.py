from rest_framework import status
from rest_framework.reverse import reverse
from json import loads
from sso.models import User
from sso.tests.base_test import BaseAPITestCase


class SSOChangePasswordTest(BaseAPITestCase):
    # change password route should change the password (if it is valid)
    def test_new_password_valid(self):
        resp = self.client2.put(
            reverse('sso:change_password'),
            {
                'current_password': '2097152#',
                'new_password': 'somenewvalidpw',
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        user = User.objects.get(username='user2')
        self.assertTrue(user.check_password('somenewvalidpw'))
        self.assertEqual(resp.get('Content-Type'), 'application/json')

    # do not allow password change if new password is too weak
    def test_new_password_invalid_1(self):
        resp = self.client2.put(
            reverse('sso:change_password'),
            {
                'current_password': '2097152#',
                'new_password': 'user2',
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertIsNotNone(resp_json, 'errors')

    # do not allow password change if new password is too weak
    def test_new_password_invalid_2(self):
        resp = self.client2.put(
            reverse('sso:change_password'),
            {
                'current_password': '2097152#',
                'new_password': '12345678',
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertIsNotNone(resp_json, 'errors')

    # do not allow password to be changed if old password is different
    def test_new_password_invalid_3(self):
        resp = self.client2.put(
            reverse('sso:change_password'),
            {
                'current_password': 'idklol',
                'new_password': '12345678',
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertIsNotNone(resp_json, 'errors')


class SSOForgotPassword(BaseAPITestCase):
    # email is unregistered
    def test_email_invalid(self):
        resp = self.client.post(
            reverse('sso:forgot_password'),
            {
                'email': 'user4@e.ntu.edu.sg',
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(resp.get('Content-Type'), 'application/json')
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['detail'], 'Not found.')

    # if valid email, custom token should be generated and email sent
    def test_email_valid(self):
        resp = self.client.post(
            reverse('sso:forgot_password'),
            {
                'email': 'USeR1@e.ntu.edu.sg',
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.get('Content-Type'), 'application/json')
        user = User.objects.get(username='user1')
        self.assertIsNotNone(user.custom_token)
        self.assertIsNotNone(user.token_expiry_date)
