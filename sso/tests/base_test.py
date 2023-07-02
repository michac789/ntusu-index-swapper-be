from json import loads
from rest_framework.test import APIClient, APITestCase
from rest_framework.reverse import reverse
from sso.models import User


class BaseAPITestCase(APITestCase):
    '''
    Inherits from rest_framework APITestCase,
    provides setUpTestData class method that has 3 users
    (user1x as superuser, user2x & user3x as regular users),
    3 different clients for testing purpose as follows:
    Client 1 -> superuser (logged in as user1)
    Client 2 -> regular user (logged in as user2)
    Client 3 -> unauthorized / anonymous user (not logged in)
    '''
    @classmethod
    def setUpTestData(self):
        self.user1 = User.objects.create_superuser(
            username='user1x',
            password='123',
            email='user1x@mail.com',
        )
        self.user2 = User.objects.create_user(
            username='user2x',
            password='456',
            email='user2x@mail.com',
        )
        self.user3 = User.objects.create_user(
            username='user3x',
            password='789',
            email='user3x@mail.com'
        )
        self.client1 = APIClient()
        self.client2 = APIClient()
        self.client3 = APIClient()
        resp1 = self.client1.post(
            reverse('sso:token_obtain_pair'),
            {
                'username': 'user1x',
                'password': '123'
            },
            format='json'
        )
        token1 = loads(resp1.content.decode('utf-8'))['access']
        self.client1.credentials(HTTP_AUTHORIZATION='Bearer ' + token1)
        resp2 = self.client2.post(
            reverse('sso:token_obtain_pair'),
            {
                'username': 'user2x',
                'password': '456'
            },
            format='json'
        )
        token2 = loads(resp2.content.decode('utf-8'))['access']
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + token2)
