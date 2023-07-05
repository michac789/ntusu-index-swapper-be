from json import loads
from indexswapper.models import SwapRequest
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
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '99999',
            'wanted_indexes': ['70185', '70186'],
        })
        self.assertEqual(resp.status_code, 404)

    def test_fail_bad_request_format_3(self):
        # some index in wanted_indexes are invalid
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '7018100000',
            'wanted_indexes': ['70185', 'XX'],
        })
        self.assertEqual(resp.status_code, 400)

    def test_fail_bad_request_format_4(self):
        # some index in wanted_indexes are of a different course
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70181',
            'wanted_indexes': ['70200', '70186'],
        })
        self.assertEqual(resp.status_code, 400)

    def test_fail_bad_request_format_5(self):
        # wanted_indexes is empty
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70181',
            'wanted_indexes': [],
        })
        self.assertEqual(resp.status_code, 400)

    def test_fail_bad_request_format_6(self):
        # wanted_indexes same as current index
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70181',
            'wanted_indexes': ['70181'],
        })
        self.assertEqual(resp.status_code, 400)

    def test_fail_conflict(self):
        # user has created a swap request with the same index, and the status is S or W
        self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70200',
            'wanted_indexes': ['70201'],
        })
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70200',
            'wanted_indexes': ['70202', '70203'],
        })
        self.assertEqual(resp.status_code, 409)

    def test_success(self):
        resp = self.client1.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70181',
            'wanted_indexes': ['70185', '70186'],
        })
        self.assertEqual(resp.status_code, 201)
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertIn('id', resp_json)
        self.assertEqual(resp_json['contact_info'],
                         'sample_mail@mail.com')
        self.assertEqual(resp_json['contact_type'], 'E')
        self.assertEqual(resp_json['course_code'], 'MH1100')
        self.assertEqual(resp_json['course_name'], 'CALCULUS I')
        self.assertEqual(resp_json['current_index'], '70181')
        self.assertEqual(resp_json['wanted_indexes'], ['70185', '70186'])
        self.assertEqual(list(resp_json.keys()), [
                         'contact_info', 'contact_type', 'wanted_indexes',
                         'course_code', 'course_name', 'current_index', 'id'])


class SwapRequestCreateAlgoTestCase(IndexSwapperBaseTestCase):
    ENDPOINT = '/indexswapper/swaprequest/'

    def test_algo_pair_found_1(self):
        resp = self.client2.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70220',
            'wanted_indexes': ['70219', '70221'],
        })
        resp_json = loads(resp.content.decode('utf-8'))
        swaprequest_id = resp_json['id']
        instance = SwapRequest.objects.get(id=swaprequest_id)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(instance.status, SwapRequest.Status.WAITING)
        self.assertEqual(instance.index_gained, '70221')
        self.assertEqual(instance.pair.id, 2)
        self.assertEqual(instance.pair.status, SwapRequest.Status.WAITING)
        self.assertEqual(instance.pair.index_gained, '70220')
        self.assertIsNotNone(instance.pair.datetime_found)
        self.assertIsNotNone(instance.datetime_added)
        self.assertIsNotNone(instance.datetime_found)
        self.assertEqual(instance.datetime_found, instance.pair.datetime_found)

    def test_algo_pair_found_2(self):
        resp = self.client2.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70204',
            'wanted_indexes': ['70195', '70201', '70205'],
        })
        resp_json = loads(resp.content.decode('utf-8'))
        swaprequest_id = resp_json['id']
        instance = SwapRequest.objects.get(id=swaprequest_id)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(instance.status, SwapRequest.Status.WAITING)
        self.assertEqual(instance.index_gained, '70195')
        self.assertEqual(instance.pair.id, 4)
        self.assertEqual(instance.pair.status, SwapRequest.Status.WAITING)
        self.assertEqual(instance.pair.index_gained, '70204')
        self.assertIsNotNone(instance.pair.datetime_found)
        self.assertIsNotNone(instance.datetime_added)
        self.assertIsNotNone(instance.datetime_found)
        self.assertEqual(instance.datetime_found, instance.pair.datetime_found)

    def test_algo_pair_not_found_1(self):
        resp = self.client2.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70220',
            'wanted_indexes': ['70219'],
        })
        resp_json = loads(resp.content.decode('utf-8'))
        swaprequest_id = resp_json['id']
        instance = SwapRequest.objects.get(id=swaprequest_id)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(instance.status, SwapRequest.Status.SEARCHING)
        self.assertEqual(instance.index_gained, '')
        self.assertIsNone(instance.datetime_found)
        self.assertIsNone(instance.pair)
        self.assertIsNotNone(instance.datetime_added)

    def test_algo_pair_not_found_2(self):
        resp = self.client2.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70196',
            'wanted_indexes': ['70195', '70201', '70205'],
        })
        resp_json = loads(resp.content.decode('utf-8'))
        swaprequest_id = resp_json['id']
        instance = SwapRequest.objects.get(id=swaprequest_id)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(instance.status, SwapRequest.Status.SEARCHING)
        self.assertEqual(instance.index_gained, '')
        self.assertIsNone(instance.datetime_found)
        self.assertIsNone(instance.pair)
        self.assertIsNotNone(instance.datetime_added)

    def test_algo_pair_not_found_3(self):
        # should not be paired with SwapRequest that is WAITING
        resp = self.client2.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70182',
            'wanted_indexes': ['70181'],
        })
        resp_json = loads(resp.content.decode('utf-8'))
        swaprequest_id = resp_json['id']
        instance = SwapRequest.objects.get(id=swaprequest_id)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(instance.status, SwapRequest.Status.SEARCHING)
        self.assertEqual(instance.index_gained, '')
        self.assertIsNone(instance.datetime_found)
        self.assertIsNone(instance.pair)
        self.assertIsNotNone(instance.datetime_added)

    def test_algo_pair_not_found_4(self):
        # should not be paired with SwapRequest that is COMPLETED
        resp = self.client2.post(self.ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70217',
            'wanted_indexes': ['70211', '70212'],
        })
        resp_json = loads(resp.content.decode('utf-8'))
        swaprequest_id = resp_json['id']
        instance = SwapRequest.objects.get(id=swaprequest_id)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(instance.status, SwapRequest.Status.SEARCHING)
        self.assertEqual(instance.index_gained, '')
        self.assertIsNone(instance.datetime_found)
        self.assertIsNone(instance.pair)
        self.assertIsNotNone(instance.datetime_added)
