from django.test import TestCase


class BasicServerTest(TestCase):
    def test_server(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_swagger(self):
        response = self.client.get('/swagger/')
        self.assertEqual(response.status_code, 200)
