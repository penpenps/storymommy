# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from Consts import DATETIME_FORMAT


def format_datetime_str(dt):
    if isinstance(dt, datetime):
        return dt.strftime(DATETIME_FORMAT)
    else:
        return "-"



