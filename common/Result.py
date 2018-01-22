# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Result(object):
    def __init__(self, code=None, msg=None):
        self.code = code
        self.msg = msg

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg
        }
