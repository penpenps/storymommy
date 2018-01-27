# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from models import Group
from admin import create_group, check_group_exist, check_name_exist, update_group_info, remove_group, get_all_groups
from backend.admin import create_user
import logging.config
from common.LoggerConfig import LOGGING

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)


class GroupTestCase(TestCase):
    def setUp(self):
        create_user(username="admin", name="admin", password="aaa", email="example@admin.com", phone="123")
        create_user(username="admin2", name="admin2", password="bbb", email="example@admin.com", phone="123")
        create_group("group1", admin_username="admin")

    def test_create_group(self):
        create_group("group2", admin_username="admin")
        group = Group.objects.get(name="group2")
        self.assertEqual(group.name, "group2")
        self.assertEqual(group.admin.username, "admin")
        self.assertEqual(group.admin.first_name, "admin")
        self.assertEqual(group.admin.email, "example@admin.com")
        self.assertEqual(group.admin.last_name, "123")

    def test_check_exist(self):
        self.assertTrue(check_name_exist("group1"))
        group = Group.objects.get(name="group1")
        self.assertTrue(check_group_exist(group.id))
        self.assertFalse(check_name_exist("group3"))

    def test_update_group_info(self):
        group = Group.objects.get(name="group1")
        _id = group.id
        update_group_info(_id, "group3", "admin2")
        group = Group.objects.get(id=_id)
        self.assertEqual(group.name, "group3")
        self.assertEqual(group.admin.username, "admin2")

    def test_remove_group(self):
        group = Group.objects.get(name="group1")
        _id = group.id
        remove_group(_id)
        self.assertFalse(check_name_exist("group1"))

    def test_get_all_groups(self):
        create_group("group2", admin_username="admin2")
        self.assertEqual(len(get_all_groups()), 2)
        self.assertEqual(len(get_all_groups("admin")), 1)
        self.assertEqual(len(get_all_groups("admin2")), 1)
        self.assertEqual(len(get_all_groups("admin3")), 0)
