import base64
import json
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

class GuestUserTests(APITestCase):

    def test_guest_user_registration(self):
        url = reverse('register_guest_user')
        response = self.client.post(url, data={})
        user = get_user_model().objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_name'], user.get_username())
        self.assertEqual(response.data['is_guest'], True)
        self.assertEqual(response.data['id'], user.id)
       


    def test_guest_user_login(self):

        url = reverse('register_guest_user')
        response = self.client.post(url, data={})
        user = get_user_model().objects.last()

        url = reverse('login')
        response = self.client.post(url, data={
            'user_name': user.user_name,
            'password': 'guest'
        })

        access_token = response.data['access']
        header, payload, signature = access_token.split('.')
        decoded_payload = base64.b64decode(f'{payload}==')
        payload_data = json.loads(decoded_payload)
        print(payload_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['refresh'])
        