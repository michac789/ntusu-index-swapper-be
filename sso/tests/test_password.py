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
