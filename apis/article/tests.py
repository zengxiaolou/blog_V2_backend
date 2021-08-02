from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from loguru import logger as log


class UserTests(APITestCase):

    def test_create_account(self):
        url = reverse("article:archive-list")
        log.debug(url)
        response = self.client.get(url, format="json")
        log.debug(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)