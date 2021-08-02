from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Comment
from loguru import logger as log


class UserTests(APITestCase):

    def test_create_account(self):
        log.debug("url")
        url = 'api/(?P<version>[v1|2]+)/operations/user-like/$'
        log.debug(url)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
