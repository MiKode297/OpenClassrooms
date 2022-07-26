import json
import logging
import os
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext as _
from django.test import Client, TestCase

from rest_framework import status

from appz.classrooms import models


# Get an instance of a logger
logger = logging.getLogger(__name__)


class TestUserSign(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass


    # [TODO](mtt) check assignment with 2 different partners
    def test_api_user_signin(self):

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/?next=",
            response.url
        )

        response = self.client.get(reverse("api_index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/?next=",
            response.url
        )

        username = "user01"
        email = "user01@domain.com"
        password = "$user01_pwd$"

        user = User.objects.create_user(username=username,
            email=email, password=password
        )
        # user.first_name = first_name
        # user.last_name = last_name
        user.save()
        logger.warning(f"THE user: {user}")
        print(f"THE user: {user}")


        # headers = {"HTTP_Authorization": settings.TEST_NEW_SMARTDOCS_API_KEY}
        data = {"username": username, "email": email, "password": password}

        response = self.client.post(reverse("signin"), data=data)
        print(f"WWAAAAAAAAAAAAAAAAAAAAa: {response}")
        self.assertEqual(response.status_code, 200)

        content_dct = json.loads(response.content)
        print(f"WWAAAAAAAAAAAAAAAAAAAAa: {content_dct})")
        logger.warning(f"Sign in response: {response}")
        print(f"Sign in response: {response}")

        # return user ID
        # token = Token.objects.create(user=user)

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)

        expected_content_dct = {
            "email": email,
            # "first_name": first_name,
            # "last_name":
            #  last_name
        }
        self.assertEquals(content_dct["email"], expected_content_dct["email"])

        logger.debug(f"TOKEN from signup: {content_dct['token']}")
        self.assertIsInstance(content_dct["token"], str)

        # user = CustomUser.objects.get(email=email)
        # self.assertTrue(user.is_authenticated)
        # self.assertTrue(user.is_active)

        # user = authenticate(email=email, password=password)
        # self.assertIsNotNone(user)

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/?next=",
            response.url
        )

        headers = {"HTTP_Authorization": f"Token {content_dct['token']}"}
        logger.warning(headers)
        response = self.client.get(reverse("index"), **headers)
        logger.warning(f"{response}")
        logger.warning(f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA {0}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, 405)
        self.assertEqual(response.status_code, 405)
