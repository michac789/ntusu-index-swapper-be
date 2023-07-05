from json import loads
from unittest.mock import patch
from indexswapper.models import SwapRequest
from indexswapper.tests.base_test import IndexSwapperBaseTestCase


class SwapRequestSearchAnotherTestCase(IndexSwapperBaseTestCase):
    ENDPOINT = (
        lambda _, id: f'/indexswapper/swaprequest/{id}/search_another/')
    CREATE_ENDPOINT = '/indexswapper/swaprequest/'

    def test_fail_unauthorized(self):
        resp = self.client3.patch(self.ENDPOINT(1))
        self.assertEqual(resp.status_code, 401)

    def test_fail_not_found(self):
        resp = self.user1c.patch(self.ENDPOINT(99999))
        self.assertEqual(resp.status_code, 404)

    def test_fail_forbidden(self):
        resp = self.user1c.patch(self.ENDPOINT(3))
        self.assertEqual(resp.status_code, 403)

    def test_fail_not_waiting_status_1(self):
        # still searching
        resp = self.user1c.patch(self.ENDPOINT(2))
        self.assertEqual(resp.status_code, 400)

    def test_fail_not_waiting_status_2(self):
        # completed status
        resp = self.user4c.patch(self.ENDPOINT(6))
        self.assertEqual(resp.status_code, 400)

    def test_fail_cooldown_unfinished(self):
        # note: we only simply test failure if we search another right after making the first swaprequest
        # assume that the `COOLDOWN_HOURS` in `verify_cooldown` decorator is at least 1 hour
        resp = self.client1.post(self.CREATE_ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70220',
            'wanted_indexes': ['70221', '70217'],
        })
        self.assertEqual(resp.status_code, 201)
        resp_json = loads(resp.content.decode('utf-8'))
        resp2 = self.client1.patch(self.ENDPOINT(resp_json['id']))
        self.assertEqual(resp2.status_code, 400)
        resp_json_2 = loads(resp2.content.decode('utf-8'))
        self.assertEqual(resp_json_2['error'], 'waiting for cooldown')
        self.assertGreater(float(resp_json_2['time_left']), 0)
        self.assertEqual(list(resp_json_2.keys()), ['error', 'time_left'])

    def test_success_pair_found(self):
        SWAPREQUEST_ID = 1
        instance = SwapRequest.objects.get(id=SWAPREQUEST_ID)
        old_pair_id = instance.pair.id
        new_sr_resp = self.client2.post(self.CREATE_ENDPOINT, {
            'contact_info': 'sample_mail@mail.com',
            'contact_type': 'E',
            'current_index_num': '70184',
            'wanted_indexes': ['70181', '70192'],
        })
        resp = self.user1c.patch(self.ENDPOINT(SWAPREQUEST_ID))
        self.assertEqual(resp.status_code, 200)
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json, 'ok')
        instance = SwapRequest.objects.get(id=SWAPREQUEST_ID)
        self.assertEqual(instance.status, SwapRequest.Status.WAITING)
        self.assertEqual(instance.index_gained, '70184')
        self.assertEqual(instance.pair.id, new_sr_resp.data['id'])
        self.assertEqual(instance.pair.status, SwapRequest.Status.WAITING)
        self.assertEqual(instance.pair.index_gained, '70181')
        self.assertIsNotNone(instance.pair.datetime_found)
        self.assertIsNotNone(instance.datetime_added)
        self.assertIsNotNone(instance.datetime_found)
        self.assertEqual(instance.datetime_found, instance.pair.datetime_found)
        old_pair = SwapRequest.objects.get(id=old_pair_id)
        self.assertEqual(old_pair.pair.id, SWAPREQUEST_ID)
        self.assertEqual(old_pair.status, SwapRequest.Status.WAITING)

    def test_success_pair_not_found(self):
        SWAPREQUEST_ID = 1
        instance = SwapRequest.objects.get(id=SWAPREQUEST_ID)
        old_pair_id = instance.pair.id
        resp = self.user1c.patch(self.ENDPOINT(SWAPREQUEST_ID))
        self.assertEqual(resp.status_code, 200)
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json, 'ok')
        instance = SwapRequest.objects.get(id=SWAPREQUEST_ID)
        self.assertEqual(instance.status, SwapRequest.Status.SEARCHING)
        self.assertEqual(instance.index_gained, '')
        self.assertIsNone(instance.datetime_found)
        self.assertIsNone(instance.pair)
        self.assertIsNotNone(instance.datetime_added)
        old_pair = SwapRequest.objects.get(id=old_pair_id)
        self.assertEqual(old_pair.pair.id, SWAPREQUEST_ID)
        self.assertEqual(old_pair.status, SwapRequest.Status.WAITING)


class SwapRequestMarkCompleteTestCase(IndexSwapperBaseTestCase):
    ENDPOINT = (lambda _, id: f'/indexswapper/swaprequest/{id}/mark_complete/')

    def test_fail_unauthorized(self):
        resp = self.client3.patch(self.ENDPOINT(1))
        self.assertEqual(resp.status_code, 401)

    def test_fail_not_found(self):
        resp = self.user1c.patch(self.ENDPOINT(99999))
        self.assertEqual(resp.status_code, 404)

    def test_fail_forbidden(self):
        resp = self.user1c.patch(self.ENDPOINT(3))
        self.assertEqual(resp.status_code, 403)

    def test_fail_not_waiting_status_1(self):
        # already completed
        resp = self.user4c.patch(self.ENDPOINT(6))
        self.assertEqual(resp.status_code, 400)

    def test_fail_not_waiting_status_2(self):
        # still searching
        resp = self.user1c.patch(self.ENDPOINT(2))
        self.assertEqual(resp.status_code, 400)

    @patch('indexswapper.utils.email.send_swap_completed')
    def test_success(self, mock_func):
        resp = self.user1c.patch(self.ENDPOINT(1))
        self.assertEqual(resp.status_code, 200)
        swap_request = SwapRequest.objects.get(id=1)
        self.assertEqual(swap_request.status, SwapRequest.Status.COMPLETED)
        mock_func.assert_called_once()


class SwapRequestCancelSwapTestCase(IndexSwapperBaseTestCase):
    ENDPOINT = (lambda _, id: f'/indexswapper/swaprequest/{id}/cancel_swap/')

    def test_fail_unauthorized(self):
        resp = self.client3.patch(self.ENDPOINT(1))
        self.assertEqual(resp.status_code, 401)

    def test_fail_not_found(self):
        resp = self.user1c.patch(self.ENDPOINT(99999))
        self.assertEqual(resp.status_code, 404)

    def test_fail_forbidden(self):
        resp = self.user1c.patch(self.ENDPOINT(3))
        self.assertEqual(resp.status_code, 403)

    def test_fail_completed_status(self):
        # already completed
        resp = self.user4c.patch(self.ENDPOINT(6))
        self.assertEqual(resp.status_code, 400)

    def test_success_1(self):
        # TODO - do this with 'CANCEL' status issue #24
        pass

    def test_success_2(self):
        # TODO - do this with 'CANCEL' status issue #24
        pass
