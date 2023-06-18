from json import loads
from sso.tests.base_test import BaseAPITestCase


class CourseIndexListTestCase(BaseAPITestCase):
    ENDPOINT = '/indexswapper/courseindex/'
    fixtures = ['sample_course_index_small.json']

    def test_success_default(self):
        resp = self.client3.get(self.ENDPOINT)
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 33)
        self.assertEqual(resp_json['total_pages'], 4)
        self.assertEqual(len(resp_json['results']), 10)

    # TODO - make more test cases for qp


class CourseIndexRetrieveTestCase(BaseAPITestCase):
    ENDPOINT = (lambda _, index: f'/indexswapper/courseindex/{index}/')
    fixtures = ['sample_course_index_small.json']

    def test_fail_invalid_index(self):
        resp = self.client3.get(self.ENDPOINT('99999'))
        print(resp)
        self.assertEqual(resp.status_code, 404)

    def test_success_default(self):
        resp = self.client3.get(self.ENDPOINT('70181'))
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['code'], 'MH1100')
        self.assertEqual(resp_json['name'], 'CALCULUS I')
        self.assertEqual(list(resp_json.keys()), [
                         'id', 'code', 'name', 'index', 'datetime_added',
                         'pending_count', 'information_data'])
        self.assertEqual(len(resp_json['information_data']), 18)
        self.assertEqual(list(resp_json['information_data'][0].keys()),
                         ['type', 'group', 'day', 'time', 'venue', 'remark'])


class CourseIndexGetCoursesTestCase(BaseAPITestCase):
    ENDPOINT = '/indexswapper/courseindex/get_courses/'
    fixtures = ['sample_course_index_small.json']

    def test_success_default(self):
        resp = self.client3.get(self.ENDPOINT)
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 3)
        self.assertEqual(resp_json['total_pages'], 1)
        self.assertEqual(len(resp_json['results']), 3)
        self.assertEqual(resp_json['results'][0]['code'], 'MH1100')
        self.assertEqual(resp_json['results'][1]['code'], 'MH1200')
        self.assertEqual(resp_json['results'][2]['code'], 'MH1300')
        self.assertEqual(resp_json['results'][0]['name'], 'CALCULUS I')

    def test_success_qp_pagination(self):
        resp = self.client3.get(self.ENDPOINT, {
            'page_size': 2,
            'page': 2,
        })
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 3)
        self.assertEqual(resp_json['total_pages'], 2)
        self.assertEqual(len(resp_json['results']), 1)
        self.assertEqual(resp_json['results'][0]['code'], 'MH1300')

    def test_success_qp_ordering(self):
        resp = self.client3.get(self.ENDPOINT, {
            'page_size': 1,
            'page': 1,
            'ordering': '-name'
        })
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 3)
        self.assertEqual(resp_json['total_pages'], 3)
        self.assertEqual(len(resp_json['results']), 1)
        self.assertEqual(resp_json['results'][0]['code'], 'MH1200')

    def test_success_qp_search(self):
        resp = self.client3.get(self.ENDPOINT, {
            'name__icontains': 'calcu',
        })
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 1)
        self.assertEqual(resp_json['total_pages'], 1)
        self.assertEqual(len(resp_json['results']), 1)
        self.assertEqual(resp_json['results'][0]['code'], 'MH1100')


class CourseIndexGetIndexesTestCase(BaseAPITestCase):
    ENDPOINT = (
        lambda _, course_code: f'/indexswapper/courseindex/get_indexes/{course_code}/')
    fixtures = ['sample_course_index_small.json']

    def test_fail_invalid_course(self):
        resp = self.client3.get(self.ENDPOINT('ZZ9999'))
        self.assertEqual(resp.status_code, 404)

    def test_success_default(self):
        resp = self.client3.get(self.ENDPOINT('MH1100'))
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(len(resp_json), 12)
        self.assertEqual(list(resp_json[0].keys()), [
                         'index', 'pending_count', 'information'])
        self.assertEqual(list(resp_json[0]['information'][0].keys()), [
                         'type', 'group', 'day', 'time', 'venue', 'remark'])
