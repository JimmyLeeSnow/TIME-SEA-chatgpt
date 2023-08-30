# -*- coding: utf-8 -*-
import hmac
import json
import base64
import logging

from django.conf import settings
from utils.jsonResponse import SuccessResponse, ErrorResponse
from utils.common import REGEX_MOBILE, get_parameter_dic, ast_convert
from utils.textmoderation import textmoderation
from system.models import Users, TextDetection

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import F

logger = logging.getLogger(__name__)

class UserTokenCheckView:
    """
    通用token解析返回auth
    """
    @staticmethod
    def token_check(request):
        # 获取token
        token = request.headers.get('Authorization')
        # 从第七个字符开始截取到末尾
        if token.startswith('Bearer '):
            token = token[7:]
        if token != "null":
            # 根据 SA-Token 的签名算法生成签名
            header_b64, payload_b64, signature_b64 = token.split('.')
            header = json.loads(base64.urlsafe_b64decode(header_b64 + '=='))
            payload = json.loads(base64.urlsafe_b64decode(payload_b64 + '=='))
            signature = base64.urlsafe_b64decode(signature_b64 + '==')
            SECRET_KEY = getattr(settings, 'SECRET_KEY', None)
            # 根据 SA-Token 的签名算法生成验证签名的密钥
            key = SECRET_KEY.encode('utf-8')
            # 计算签名
            expected_signature = hmac.new(key, (header_b64 + '.' + payload_b64).encode('utf-8'), digestmod='sha256').digest()
            # 验证签名是否匹配
            if signature != expected_signature:
                raise ValueError('token校验失败，请不要模拟接口使用')

            return payload
