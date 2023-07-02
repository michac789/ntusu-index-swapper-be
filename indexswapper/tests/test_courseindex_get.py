from json import loads
from sso.tests.base_test import BaseAPITestCase


class CourseIndexListTestCase(BaseAPITestCase):
    ENDPOINT = '/indexswapper/courseindex/'
    fixtures = ['sample_course_index_small.json']

    def test_fail_not_found_page(self):
        resp = self.client3.get(self.ENDPOINT, {
            'page': 999,
        })
        self.assertEqual(resp.status_code, 404)
        resp = self.client3.get(self.ENDPOINT, {
            'page': 0,
        })
        self.assertEqual(resp.status_code, 404)
        resp = self.client3.get(self.ENDPOINT, {
            'page': -1,
        })
        self.assertEqual(resp.status_code, 404)

    def test_success_default(self):
        resp = self.client3.get(self.ENDPOINT)
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 33)
        self.assertEqual(resp_json['total_pages'], 4)
        self.assertEqual(len(resp_json['results']), 10)

    def test_success_qp_pagination(self):
        resp = self.client3.get(self.ENDPOINT, {
            'page_size': 2,
            'page': 5,
        })
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 33)
        self.assertEqual(resp_json['total_pages'], 17)
        self.assertEqual(len(resp_json['results']), 2)
        self.assertEqual(resp_json['results'][0]['code'], 'MH1100')
        self.assertEqual(resp_json['results'][1]['code'], 'MH1100')

    def test_success_qp_code_icontains(self):
        resp = self.client3.get(self.ENDPOINT, {
            'code__icontains': '1100'
        })
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 12)
        self.assertEqual(resp_json['total_pages'], 2)
        self.assertEqual(resp_json['results'][0]['code'], 'MH1100')

    def test_success_qp_name_icontains(self):
        resp = self.client3.get(self.ENDPOINT, {
            'name__icontains': 'math'
        })
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 11)
        self.assertEqual(resp_json['total_pages'], 2)
        self.assertEqual(resp_json['results'][0]['code'], 'MH1300')

    def test_success_qp_index(self):
        resp = self.client3.get(self.ENDPOINT, {
            'index': '70218'
        })
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 1)
        self.assertEqual(resp_json['total_pages'], 1)
        self.assertEqual(resp_json['results'][0]['code'], 'MH1300')
        # TODO - assert pending count (after sample data is finalized)

    # TODO - make test for pending_count_lt qp

    # TODO - make test for pending_count_gt qp

    def test_qp_ordering_1(self):
        resp = self.client3.get(self.ENDPOINT, {
            'ordering': 'index',
        })
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 33)
        self.assertEqual(resp_json['total_pages'], 4)
        self.assertEqual(resp_json['results'][0]['index'], '70181')
        self.assertEqual(resp_json['results'][1]['index'], '70182')
        self.assertEqual(resp_json['results'][2]['index'], '70183')

    def test_qp_ordering_2(self):
        resp = self.client3.get(self.ENDPOINT, {
            'ordering': '-index',
        })
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 33)
        self.assertEqual(resp_json['total_pages'], 4)
        self.assertEqual(resp_json['results'][0]['index'], '70221')
        self.assertEqual(resp_json['results'][1]['index'], '70220')
        self.assertEqual(resp_json['results'][2]['index'], '70219')

    def test_qp_ordering_3(self):
        resp = self.client3.get(self.ENDPOINT, {
            'ordering': '-name',
            'page_size': 20,
        })
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['count'], 33)
        self.assertEqual(resp_json['total_pages'], 2)
        self.assertEqual(resp_json['results'][0]['name'], 'LINEAR ALGEBRA I')
        self.assertEqual(resp_json['results'][19]
                         ['name'], 'FOUNDATIONS OF MATHEMATICS')


class CourseIndexRetrieveTestCase(BaseAPITestCase):
    ENDPOINT = (lambda _, index: f'/indexswapper/courseindex/{index}/')
    fixtures = ['sample_course_index_small.json']

    def test_fail_invalid_index(self):
        resp = self.client3.get(self.ENDPOINT('99999'))
        self.assertEqual(resp.status_code, 404)

    def test_success_default(self):
        resp = self.client3.get(self.ENDPOINT('70181'))
        resp_json = loads(resp.content.decode('utf-8'))
        self.assertEqual(resp_json['code'], 'MH1100')
        self.assertEqual(resp_json['name'], 'CALCULUS I')
        self.assertEqual(list(resp_json.keys()), [
                         'id', 'code', 'name', 'index', 'datetime_added',
                         'information_data'])
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
                         'index', 'information'])
        self.assertEqual(list(resp_json[0]['information'][0].keys()), [
                         'type', 'group', 'day', 'time', 'venue', 'remark'])
