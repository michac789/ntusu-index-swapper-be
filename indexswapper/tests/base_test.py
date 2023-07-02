from rest_framework.test import APIClient
from sso.models import User
from sso.tests.base_test import BaseAPITestCase


class IndexSwapperBaseTestCase(BaseAPITestCase):
    fixtures = ['sample_user.json', 'sample_course_index_small.json',
                'sample_swap_request_small.json']

    @classmethod
    def setUpTestData(self):
        super().setUpTestData()
        self.superuser = User.objects.get(username='superuser')
        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='user2')
        self.user3 = User.objects.get(username='user3')
        self.user4 = User.objects.get(username='user4')
        self.user5 = User.objects.get(username='user5')
        self.user1c = APIClient()
        self.user1c.force_authenticate(user=self.user1)
        self.user2c = APIClient()
        self.user2c.force_authenticate(user=self.user2)
        self.user3c = APIClient()
        self.user3c.force_authenticate(user=self.user3)
        self.user4c = APIClient()
        self.user4c.force_authenticate(user=self.user4)
        self.user5c = APIClient()
        self.user5c.force_authenticate(user=self.user5)
