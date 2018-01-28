# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from backend.admin import create_user
from group.admin import create_group
from admin import create_volunteer, update_volunteer_info, check_volunteer_exist, remove_volunteer
from group.models import Group
from volunteer.models import Volunteer
import logging.config
from common.LoggerConfig import LOGGING

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)


class VolunteerTestCase(TestCase):
    def setUp(self):
        create_user(username="admin", name="admin", password="aaa", email="example@admin.com", phone="123")
        create_group("group1", admin_username="admin")
        create_group("group2", admin_username="admin")

    def test_create_volunteer(self):
        group = Group.objects.get(name="group1")
        create_volunteer("admin", "123456", "xiaoming", "1380000", cert_number="abc123", year=10, group_id=group.id)
        v = Volunteer.objects.get(openid='123456')
        self.assertEqual(v.creator.username, "admin")
        self.assertEqual(v.group.name, "group1")
        self.assertEqual(v.phone, "1380000")
        self.assertEqual(v.cert_number, "abc123")
        self.assertEqual(v.year, 10)

    def test_update_volunteer(self):
        group = Group.objects.get(name="group1")
        create_volunteer("admin", "123456", "xiaoming", "1380000", cert_number="abc123", year=10, group_id=group.id)
        v = Volunteer.objects.get(openid='123456')
        self.assertEqual(v.creator.username, "admin")
        self.assertEqual(v.group.name, "group1")
        self.assertEqual(v.phone, "1380000")
        self.assertEqual(v.cert_number, "abc123")
        self.assertEqual(v.year, 10)

        group = Group.objects.get(name="group2")
        update_volunteer_info("123456", "xiaoli", "1381111", "def456", 5, group.id)
        v = Volunteer.objects.get(openid='123456')
        self.assertEqual(v.creator.username, "admin")
        self.assertEqual(v.name, "xiaoli")
        self.assertEqual(v.group.name, "group2")
        self.assertEqual(v.phone, "1381111")
        self.assertEqual(v.cert_number, "def456")
        self.assertEqual(v.year, 5)

    def test_check_volunteer(self):
        group = Group.objects.get(name="group1")
        create_volunteer("admin", "123456", "xiaoming", "1380000", cert_number="abc123", year=10, group_id=group.id)
        self.assertTrue(check_volunteer_exist("123456"))
        self.assertFalse(check_volunteer_exist("111"))

    def test_remove_volunteer(self):
        group = Group.objects.get(name="group1")
        create_volunteer("admin", "123456", "xiaoming", "1380000", cert_number="abc123", year=10, group_id=group.id)
        self.assertTrue(check_volunteer_exist("123456"))
        remove_volunteer("123456")
        self.assertFalse(check_volunteer_exist("123456"))
