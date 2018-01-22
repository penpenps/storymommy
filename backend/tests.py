# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from admin import create_user, is_username_valid
import logging.config
from common.LoggerConfig import LOGGING

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("user1", "user1@test.com", "user1password")

    def test_create_new_user(self):
        create_user("user2", "user2password", "user", "2", "user2@test.com")
        user2 = User.objects.get(username="user2")
        logger.debug("create user2")
        self.assertEqual(user2.username, "user2")
        self.assertEqual(user2.email, "user2@test.com")
        self.assertEqual(user2.first_name, "user")
        self.assertEqual(user2.last_name, "2")

    def test_is_exist_user(self):
        self.assertEqual(is_username_valid("user1"), True)
        self.assertEqual(is_username_valid("user2"), False)

