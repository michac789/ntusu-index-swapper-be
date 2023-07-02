from json import loads
from sso.tests.base_test import BaseAPITestCase


class EmailTestCase(BaseAPITestCase):
    ENDPOINT = '/sso/email-test/'

    def test_fail_unauthorized(self):
        resp = self.client3.post(self.ENDPOINT, {
            'subject': 'test subject',
            'body': 'test body',
            'recipients': ['test@e.ntu.edu.sg']
        })
        self.assertEqual(resp.status_code, 401)

    def test_fail_forbidden(self):
        resp = self.client2.post(self.ENDPOINT, {
            'subject': 'test subject',
            'body': 'test body',
            'recipients': ['test@e.ntu.edu.sg']
        })
        self.assertEqual(resp.status_code, 403)

    def test_success(self):
        resp = self.client1.post(self.ENDPOINT, {
            'subject': 'test subject',
            'body': 'test body',
            'recipients': ['test@e.ntu.edu.sg']
        })
        self.assertEqual(resp.status_code, 200)
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['ResponseMetadata']['HTTPStatusCode'], 200)
