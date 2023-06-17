from django.test import TestCase


class BasicServerTest(TestCase):
    def test_server(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
