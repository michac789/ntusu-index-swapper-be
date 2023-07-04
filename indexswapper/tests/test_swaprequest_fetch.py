from json import loads
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

    # TODO - test cooldown!

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
        resp = self.user3c.patch(self.ENDPOINT(4))
        self.assertEqual(resp.status_code, 400)

    def test_fail_not_waiting_status_2(self):
        # still searching
        resp = self.user1c.patch(self.ENDPOINT(2))
        self.assertEqual(resp.status_code, 400)

    def test_success(self):
        resp = self.user1c.patch(self.ENDPOINT(1))
        self.assertEqual(resp.status_code, 200)
        # TODO - add more assertions later!


class SwapRequestCancelSwapTestCase(IndexSwapperBaseTestCase):
    ENDPOINT = (lambda _, id: f'/indexswapper/swaprequest/{id}/cancel_swap/')
    # TODO - add test cases here later!
