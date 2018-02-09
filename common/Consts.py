# -*- coding: utf-8 -*-

SUCCESS_CODE = 0
FAILED_CODE = 1
BATCH_FAILED_CODE = 2
LOGIN_FAILED_MSG = u"用户名或密码错误"
USER_EXISTED_MSG = u"用户名已存在"
NOT_FOUND_USER_MSG = u"用户不存在"
INVALID_CSV_FILE_MSG = u"不接受非csv格式文件"
TOO_LARGE_FILE_MSG = u"导入文件不得超过2.5M"
GROUP_EXISTED_MSG = u"小组名称已存在"
NOT_FOUND_GROUP_MSG = u"小组不存在"
NOT_FOUND_VOLUNTEER_MSG = u"该志愿者不存在"
VOLUNTEER_EXIST_MSG = u"该微信已注册"
NO_PERMISSION_MSG = u"您没有权限进行该操作"
NOT_FOUND_ACTIVITY_TYPE_MSG = u"活动类型不存在"
NOT_FOUND_ACTIVITY_MSG = u"活动不存在"
NOT_FOUND_ACTIVITY_REGISTER_MSG = u"该用户未注册活动"
NOT_FOUND_TRAINING_MSG = u"该用户未注册活动"
NOT_FOUND_TRAINING_REGISTER_MSG = u"该用户未注册培训"
START_END_TIME_ERROR_MSG = u"起始时间不得晚于结束时间"
ACTIVITY_END_MSG = u"活动已开始,不得修改"
ACTIVITY_REGISTER_EXIST_MSG = u"该用户已注册该活动"
TRAINING_REGISTER_EXIST_MSG = u"该用户已注册该培训"
NOT_GIVEN_QRCODE_TYPE_MSG = u"却少参数,未指定二维码类型。"
ACTIVITY_NOT_START_MSG = u"活动还未开始"
ACTIVITY_REG_END_MSG = u"活动已结束"
PRE_ACTIVITIES_ABSENT_MSG = u"前序活动为参加,不能签到此次活动"
ACTIVITY_SIGNUP_EXIST_MSG = u"已签到该活动,不得重复签到"
UPDATE_PASSWORD_UNMATCH_MSG = u"两次输入密码不一致"
UNKNOWN_ERROR = u"系统错误"

QR_NOT_FOUND_MSG = u"无效二维码"
EXPIRED_QRCODE_MSG = u"二维码已过期"


# date and time
DATETIME_FORMAT = "%Y/%m/%d %H:%M"


# wechat
APPID = "wx11f6b12b671694d9"
SECRET = "271ea751f8dbbac1ad9de196063478a5"
