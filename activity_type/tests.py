# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from models import Group, ActivityType
from django.contrib.auth.models import User
from admin import create_activity_type, update_activity_type, remove_activity_type, get_privileged_types
from backend.admin import create_user
from group.admin import create_group, update_group_info
import logging.config
from common.LoggerConfig import LOGGING

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)


class ActivityTypeTestCase(TestCase):
    def setUp(self):
        create_user(username="admin", name="admin", password="aaa", email="example@admin.com", phone="123")
        superuser = User.objects.get(username="admin")
        superuser.is_superuser = True
        superuser.save()
        create_user(username="admin2", name="admin2", password="bbb", email="example@admin.com", phone="123")
        create_group("group1", admin_username="admin")
        create_group("group2", admin_username="admin2")

    def test_create_activity_type(self):
        group = Group.objects.get(name="group1")
        self.assertEqual(len(ActivityType.objects.all()), 0)
        create_activity_type("activity type 1", 100, False, "admin", group.id)
        ac_list = ActivityType.objects.all()
        self.assertEqual(len(ac_list), 1)
        ac = ac_list[0]
        self.assertEqual(ac.name, "activity type 1")
        self.assertEqual(ac.score, 100)
        self.assertEqual(ac.is_private, False)
        self.assertEqual(ac.creator.username, "admin")

    def test_update_activity_type(self):
        group = Group.objects.get(name="group1")
        create_activity_type("activity type 1", 100, False, "admin", group.id)
        ac = ActivityType.objects.get(name="activity type 1")
        ac_id = ac.id
        group = Group.objects.get(name="group2")
        update_activity_type(ac_id, "renamed activity type", 200, True, group.id)
        ac = ActivityType.objects.get(id=ac_id)
        self.assertEqual(ac.name, "renamed activity type")
        self.assertEqual(ac.score, 200)
        self.assertEqual(ac.is_private, True)
        self.assertEqual(ac.group.name, "group2")

    def test_remove_activity_type(self):
        group = Group.objects.get(name="group1")
        self.assertEqual(len(ActivityType.objects.all()), 0)
        create_activity_type("activity type 1", 100, False, "admin", group.id)
        ac_list = ActivityType.objects.all()
        self.assertEqual(len(ac_list), 1)
        ac = ac_list[0]
        remove_activity_type(ac.id)
        self.assertEqual(len(ActivityType.objects.all()), 0)

    def test_get_privileged_activity_type(self):
        create_activity_type("superuser's activity type", 100, False, "admin", None)
        create_activity_type("superuser's private activity type", 100, True, "admin", None)
        group = Group.objects.get(name="group1")
        create_activity_type("superuser's activity type2", 100, False, "admin", group.id)
        group2 = Group.objects.get(name="group2")
        create_activity_type("superuser's activity type3", 100, False, "admin", group2.id)
        create_activity_type("admin2's activity type", 100, False, "admin2", None)
        create_activity_type("admin2's activity type2", 100, False, "admin2", group2.id)
        create_user(username="admin3", name="admin3", password="ccc", email="example3@admin.com", phone="456")
        user1 = User.objects.get(username='admin')
        user2 = User.objects.get(username='admin2')
        user3 = User.objects.get(username='admin3')
        self.assertEqual(len(get_privileged_types(user1)), 6)
        self.assertEqual(len(get_privileged_types(user2)), 4)
        self.assertEqual(len(get_privileged_types(user3)), 1)
        # change group2's admin to user3
        update_group_info(group2.id, group2.name, "admin3")
        self.assertEqual(len(get_privileged_types(user1)), 6)
        self.assertEqual(len(get_privileged_types(user2)), 3)
        self.assertEqual(len(get_privileged_types(user3)), 3)
