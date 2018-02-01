# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from django.test import TestCase
from activity_type.models import Group, ActivityType
from activity_type.admin import create_activity_type
from django.contrib.auth.models import User
from backend.admin import create_user
from group.admin import create_group, update_group_info
from volunteer.admin import create_volunteer
from volunteer.models import Volunteer
from admin import create_activity, update_activity, get_privileged_activities, register_activity, update_activity_register_status
from models import Activity, ActivityRegister
from datetime import datetime, timedelta
from common.Consts import DATETIME_FORMAT
import logging.config
from common.LoggerConfig import LOGGING

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)


class ActivityTestCase(TestCase):
    def setUp(self):
        create_user(username="admin", name="admin", password="aaa", email="example@admin.com", phone="123")
        superuser = User.objects.get(username="admin")
        superuser.is_superuser = True
        superuser.save()
        create_user(username="admin2", name="admin2", password="bbb", email="example@admin.com", phone="123")
        create_group("group1", admin_username="admin")
        create_group("group2", admin_username="admin2")
        group = Group.objects.get(name="group1")
        create_activity_type("activity type 1", 100, False, "admin", group.id)
        create_activity_type("global activity", 100, False, "admin", None)
        group = Group.objects.get(name="group2")
        create_activity_type("activity type 2", 100, False, "admin", group.id)
        create_volunteer("admin", "123456", "xiaoming", "1380000", cert_number="abc123", year=10, group_id=group.id)

    def test_create_activity(self):
        at = ActivityType.objects.get(name="activity type 1")
        s_t = datetime.strptime("2018/01/12 08:00", DATETIME_FORMAT)
        e_t = datetime.strptime("2018/01/12 09:00", DATETIME_FORMAT)
        create_activity("activity1", at.id, s_t, e_t, "dongfang Rd.", "admin")
        self.assertEqual(len(Activity.objects.all()), 1)
        activity = Activity.objects.get(name="activity1")
        self.assertEqual(activity.start_time, s_t)
        self.assertEqual(activity.end_time, e_t)
        self.assertEqual(activity.address, "dongfang Rd.")
        self.assertEqual(activity.creator.username, "admin")
        self.assertEqual(activity.get_status(), Activity.END)

    def test_update_activity(self):
        at = ActivityType.objects.get(name="activity type 1")
        s_t = datetime.strptime("2018/01/12 08:00", DATETIME_FORMAT)
        e_t = datetime.strptime("2018/01/12 09:00", DATETIME_FORMAT)
        create_activity("activity1", at.id, s_t, e_t, "dongfang Rd.", "admin")
        self.assertEqual(len(Activity.objects.all()), 1)
        activity = Activity.objects.get(name="activity1")
        ac_id = activity.id
        s_t = datetime.now() + timedelta(hours=1)
        e_t = datetime.now() + timedelta(hours=2)
        at = ActivityType.objects.get(name="activity type 2")
        update_activity(ac_id, "updated activity", at.id, s_t, e_t, "dongfang Rd. 1217")
        activity = Activity.objects.get(id=ac_id)
        self.assertEqual(activity.name, "updated activity")
        self.assertEqual(activity.type.name, "activity type 2")
        self.assertEqual(activity.start_time, s_t)
        self.assertEqual(activity.end_time, e_t)
        self.assertEqual(activity.address, "dongfang Rd. 1217")
        self.assertEqual(activity.get_status(), Activity.NOT_START)

    def test_get_privileged_activities(self):
        at = ActivityType.objects.get(name="global activity")
        s_t = datetime.strptime("2018/01/12 08:00", DATETIME_FORMAT)
        e_t = datetime.strptime("2018/01/12 09:00", DATETIME_FORMAT)
        create_activity("activity1", at.id, s_t, e_t, "dongfang Rd.", "admin")
        create_activity_type("superuser's private activity type", 100, True, "admin", None)
        at = ActivityType.objects.get(name="superuser's private activity type")
        create_activity("private activity", at.id, s_t, e_t, "dongfang Rd.", "admin")
        group = Group.objects.get(name="group2")
        create_activity_type("group2's activity type", 100, False, "admin", group.id)
        at = ActivityType.objects.get(name="group2's activity type")
        create_activity("group2's activity", at.id, s_t, e_t, "dongfang Rd.", "admin")
        create_user(username="admin3", name="admin3", password="ccc", email="example3@admin.com", phone="456")
        user1 = User.objects.get(username='admin')
        user2 = User.objects.get(username='admin2')
        user3 = User.objects.get(username='admin3')
        self.assertEqual(len(get_privileged_activities(user1)), 3)
        self.assertEqual(len(get_privileged_activities(user2)), 2)
        self.assertEqual(len(get_privileged_activities(user3)), 1)

    def test_register_individual_activity(self):
        self.assertEqual(len(ActivityRegister.objects.all()), 0)
        at = ActivityType.objects.get(name="global activity")
        s_t = datetime.strptime("2018/01/12 08:00", DATETIME_FORMAT)
        e_t = datetime.strptime("2018/01/12 09:00", DATETIME_FORMAT)
        create_activity("activity1", at.id, s_t, e_t, "dongfang Rd.", "admin")
        activity = Activity.objects.get(name="activity1")
        register_activity(activity.id, "123456", "admin")
        self.assertEqual(len(ActivityRegister.objects.all()), 1)

    def test_update_activity_register(self):
        at = ActivityType.objects.get(name="global activity")
        s_t = datetime.strptime("2018/01/12 08:00", DATETIME_FORMAT)
        e_t = datetime.strptime("2018/01/12 09:00", DATETIME_FORMAT)
        create_activity("activity1", at.id, s_t, e_t, "dongfang Rd.", "admin")
        activity = Activity.objects.get(name="activity1")
        register_activity(activity.id, "123456", "admin")
        ra = ActivityRegister.objects.get(activity__id=activity.id, volunteer__openid="123456")
        self.assertEqual(ra.status, ActivityRegister.REGISTERED)
        update_activity_register_status(ra.id, ActivityRegister.SIGNED_UP)
        ra = ActivityRegister.objects.get(activity__id=activity.id, volunteer__openid="123456")
        self.assertEqual(ra.status, ActivityRegister.SIGNED_UP)
        update_activity_register_status(ra.id, ActivityRegister.ABSENT)
        ra = ActivityRegister.objects.get(activity__id=activity.id, volunteer__openid="123456")
        self.assertEqual(ra.status, ActivityRegister.ABSENT)
