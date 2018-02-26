# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
from activity.models import Activity, ActivityRegister
import logging
import os
from storymommy.settings import LOG_DIR
import time
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
log_file_name = os.path.join(LOG_DIR, "activity_status_update_%s.log" % time.strftime("%Y%m%d"))
handler = logging.FileHandler(log_file_name, mode='a', encoding=None, delay=False)
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


class Command(BaseCommand):
    def handle(self, *args, **options):
        registers = ActivityRegister.objects.all()
        for r in registers:
            if r.activity.end_time + datetime.timedelta(hours=1) < datetime.datetime.now() and r.status == ActivityRegister.REGISTERED:
                r.status = ActivityRegister.ABSENT
                r.save()
                log_msg = u'Update volunteer "%s" in activity "%s" status as "%s"' % (r.volunteer.name, r.activity.name, r.get_status_display())
                logger.info(log_msg)
