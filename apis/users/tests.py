from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import UserProfile
from loguru import logger as log


class UserTests(APITestCase):

    def test_create_account(self):
        url = reverse('comments')
        log.debug(url)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get().name, "apps")