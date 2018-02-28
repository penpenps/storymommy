# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from Consts import DATETIME_FORMAT, APPID, SECRET
import requests
import json
import random
import string
from django.core.urlresolvers import reverse
import qrcode
import qrcode.image.svg


def format_datetime_str(dt):
    if isinstance(dt, datetime):
        return dt.strftime(DATETIME_FORMAT)
    else:
        return "-"


def get_openid(code):
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (APPID, SECRET, code)
    response = requests.get(url)
    ret = json.loads(response.text)
    # print ret
    return ret['openid'] if 'openid' in ret else None


def get_random_str(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def get_absolute_url(qr_id):
    return reverse('backend.views.proc_qrcode', args=[str(qr_id)])


def generate_qrcode(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgFragmentImage)
    return img
