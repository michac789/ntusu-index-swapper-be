from indexswapper.models import CourseIndex
from sso.tests.base_test import BaseAPITestCase


class CourseIndexPopulateTestCase(BaseAPITestCase):
    ENDPOINT_POPULATE_DB = '/indexswapper/populate_db/'
    SAMPLE_WEB_LINK = 'https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1?acadsem=2023;1&staff_access=true&r_search_type=F&boption=Search&r_subj_code='

    def test_post_fail_unauthorized(self):
        resp = self.client3.post(self.ENDPOINT_POPULATE_DB)
        self.assertEqual(resp.status_code, 401)

    def test_post_fail_forbidden(self):
        resp = self.client2.post(self.ENDPOINT_POPULATE_DB)
        self.assertEqual(resp.status_code, 403)

    def test_post_fail_bad_request_1(self):
        resp = self.client1.post(self.ENDPOINT_POPULATE_DB, {
            'admin_key': 'invalidadminkey',
            'web_link': self.SAMPLE_WEB_LINK,
            'num_entry': 8,
        }, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_post_success(self):
        resp = self.client1.post(self.ENDPOINT_POPULATE_DB, {
            'admin_key': '12345',
            'web_link': self.SAMPLE_WEB_LINK,
            'num_entry': 8,
        }, format='json')
        self.assertEqual(resp.status_code, 201)
        instances = CourseIndex.objects.all().count()
        self.assertEqual(instances, 8)
