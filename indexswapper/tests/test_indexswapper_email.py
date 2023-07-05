'''
    This file is used to:
    - ensure email operation can be completed successfully given data of the intended structure format
    - test email stylings by sending emails to your own email (change line 18 below to test it!)
'''
from indexswapper.models import SwapRequest
from indexswapper.tests.base_test import IndexSwapperBaseTestCase
from indexswapper.utils import email
from sso.models import User


class SwapRequestEmailTestCase(IndexSwapperBaseTestCase):
    @classmethod
    def setUpTestData(self):
        super().setUpTestData()
        self.SAMPLE_USER: User = self.user3
        # change to your email to test
        self.SAMPLE_USER.email = 'yourmail@e.ntu.edu.sg'
        self.SAMPLE_USER.save()
        self.SAMPLE_SWAP_REQUEST_DATA: dict = {
            'id': 4,
            'contact_type': 'E',
            'contact_info': 'user3@mail.com',
            'course_name': 'LINEAR ALGEBRA I',
            'course_code': 'MH1200',
            'current_index': '70195',
            'wanted_indexes': ['70201', '70203', '70204'],
        }
        self.SAMPLE_SWAP_REQUEST: SwapRequest = SwapRequest.objects.get(id=4)

    def test_email_send_swap_search_creation(self):
        resp = email.send_swap_request_creation(
            self.SAMPLE_USER, self.SAMPLE_SWAP_REQUEST_DATA)
        self.assertEqual(resp['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_email_send_swap_search_another(self):
        resp = email.send_swap_search_another(
            self.SAMPLE_USER, self.SAMPLE_SWAP_REQUEST)
        self.assertEqual(resp['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_email_send_swap_completed(self):
        resp = email.send_swap_completed(
            self.SAMPLE_USER, self.SAMPLE_SWAP_REQUEST)
        self.assertEqual(resp['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_email_send_swap_cancel_self(self):
        resp = email.send_swap_cancel_self(
            self.SAMPLE_USER, self.SAMPLE_SWAP_REQUEST)
        self.assertEqual(resp['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_email_send_swap_cancel_pair(self):
        resp = email.send_swap_cancel_pair(
            self.SAMPLE_USER, self.SAMPLE_SWAP_REQUEST)
        self.assertEqual(resp['ResponseMetadata']['HTTPStatusCode'], 200)
