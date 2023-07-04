from json import loads
from indexswapper.tests.base_test import IndexSwapperBaseTestCase


class SwapRequestSearchAnotherTestCase(IndexSwapperBaseTestCase):
    ENDPOINT = (
        lambda _, id: f'/indexswapper/swaprequest/{id}/search_another/')

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

    def test_success(self):
        resp = self.user1c.patch(self.ENDPOINT(1))
        self.assertEqual(resp.status_code, 200)
        # TODO - add more assertions later!


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
