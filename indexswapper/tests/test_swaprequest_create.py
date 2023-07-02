from json import loads
from indexswapper.tests.base_test import IndexSwapperBaseTestCase


class SwapRequestCreateTestCase(IndexSwapperBaseTestCase):
    ENDPOINT = '/indexswapper/swaprequest/'

    def test_fail_unauthorized(self):
        resp = self.client3.get(self.ENDPOINT)
        self.assertEqual(resp.status_code, 401)

    def test_fail_bad_request_format_1(self):
        # missing contact info
        resp = self.client1.post(self.ENDPOINT, {
            'current_index_num': '70181',
            'wanted_indexes': ['70185', '70186'],
        })
        self.assertEqual(resp.status_code, 400)

    def test_fail_bad_request_format_2(self):
        # invalid current index
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample contact information',
            'current_index_num': '99999',
            'wanted_indexes': ['70185', '70186'],
        })
        self.assertEqual(resp.status_code, 404)

    def test_fail_bad_request_format_3(self):
        # some index in wanted_indexes are invalid
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample contact information',
            'current_index_num': '7018100000',
            'wanted_indexes': ['70185', 'XX'],
        })
        self.assertEqual(resp.status_code, 400)

    def test_fail_bad_request_format_4(self):
        # some index in wanted_indexes are of a different course
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample contact information',
            'current_index_num': '70181',
            'wanted_indexes': ['70200', '70186'],
        })
        self.assertEqual(resp.status_code, 400)

    def test_fail_bad_request_format_5(self):
        # wanted_indexes is empty
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample contact information',
            'current_index_num': '70181',
            'wanted_indexes': [],
        })
        self.assertEqual(resp.status_code, 400)

    def test_fail_bad_request_format_6(self):
        # wanted_indexes same as current index
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample contact information',
            'current_index_num': '70181',
            'wanted_indexes': ['70181'],
        })
        self.assertEqual(resp.status_code, 400)

    def test_fail_conflict(self):
        # user has created a swap request with the same index, and the status is S or W
        self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample contact information',
            'current_index_num': '70200',
            'wanted_indexes': ['70201'],
        })
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample contact information',
            'current_index_num': '70200',
            'wanted_indexes': ['70202', '70203'],
        })
        self.assertEqual(resp.status_code, 409)

    def test_success(self):
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample contact information',
            'current_index_num': '70181',
            'wanted_indexes': ['70185', '70186'],
        })
        self.assertEqual(resp.status_code, 201)
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertIn('id', resp_json)
        self.assertEqual(resp_json['contact_info'],
                         'sample contact information')
        self.assertEqual(resp_json['course_code'], 'MH1100')
        self.assertEqual(resp_json['course_name'], 'CALCULUS I')
        self.assertEqual(resp_json['current_index'], '70181')
        self.assertEqual(resp_json['wanted_indexes'], ['70185', '70186'])

    # TODO - test algorithm here
