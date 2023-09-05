# -*- coding: utf-8 -*-
import re
import json
import base64
import logging

from utils.jsonResponse import SuccessResponse, ErrorResponse
from utils.common import REGEX_MOBILE, get_parameter_dic, ast_convert
from django_redis import get_redis_connection
from utils.textmoderation import textmoderation
from system.models import Users, TextDetection

from rest_framework.views import APIView
from django.db.models import F, Q, Case, When, Value, BooleanField, IntegerField

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
            redis_conn = get_redis_connection('session')
            try:
                # 验证签名是否匹配
                payload = redis_conn.get('token:login:token:%s' % token).decode()
            except Exception as e:
                logger.error("redis连接异常错误:%s" % (str(e)))
                # 如果验证失败，则 token 无效
                raise ValueError('token校验失败，请不要模拟接口使用')

            return payload

class UserStatusDisableView(APIView):
    """
    用户违禁状态检测
    """
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        try:
            # 获取用户的信息
            parameter_dic = get_parameter_dic(request)
            email_account = parameter_dic.get('emailAccount', None)
            user_info = json.loads(parameter_dic.get('userInfo', "{}"))
            open_id = user_info.get('openId')

            # 判断用户使用的登录方式
            account = email_account if email_account not in (None, '') else open_id

            # 判断是邮箱还是open_id
            filter_condition = Q(email=account) if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', account) else Q(open_id=account)
            
            try:
                user_exists = Users.objects.filter(filter_condition).exists()

                if user_exists:
                    is_disable = Users.objects.filter(filter_condition).values('is_disable').first()
                    if is_disable['is_disable']:
                        data = {
                            'code': 4000,
                            'msg': '该账号已被封禁，请联系管理员进行解封'
                        }
                        return SuccessResponse(data=data)
                    else:
                        data = {
                            'code': 2000,
                            'msg': '该用户行为正常'
                        }
                        return SuccessResponse(data=data)
                else:
                    data = {
                        'code': 4004,
                        'msg': '用户不存在'
                    }
                    logger.error("用户不存在")
                    return SuccessResponse(data=data)
            except Exception as e:
                data = {
                    'code': 4001,
                    'msg': '请求失败'
                }
                logger.error("请求失败: %s" % str(e))
                return SuccessResponse(data=data)
        except Exception as e:
            logger.error("参数获取异常错误:%s" % (str(e)))
            return ErrorResponse(msg="文本校验出现异常，请联系管理员获取奖励~")

class ProhibitedTextDetectionView(APIView):
    """
    违禁词检测
    """
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # 检查用户身份
        payload = UserTokenCheckView.token_check(request)
        if not payload:
            return ErrorResponse(msg='token校验失败，请不要模拟接口使用')

        try:
            # 获取用户的信息
            parameter_dic = get_parameter_dic(request)
            email_account = parameter_dic['messages'].get('emailAccount', None)
            user_info = json.loads(parameter_dic['messages'].get('userInfo', "{}"))
            open_id = user_info.get('openId')
            user_type = user_info.get('type')

            # 判断用户使用的登录方式
            account = email_account if email_account not in (None, '') else open_id

            if user_type == 'ADMIN':
                # 管理员用户直接返回，文本无异常
                data = {
                    'msg': "文本无任何异常",
                    'code': 2000
                }
                return SuccessResponse(data=data)

            # 先判断违禁次数，如果大于等于10则封禁状态置为1
            Users.objects.filter(detection_counts__gte=10).update(
                is_disable=Case(
                    When(is_disable__isnull=True, then=Value(1)),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            )

            # 获取客户端IP和消息内容
            client_ip = request.META.get('REMOTE_ADDR')
            messages_data = parameter_dic['messages'].get('content')
            messages = base64.b64encode(messages_data.encode('utf-8')).decode('utf-8')

            try:
                # 腾讯云文本校验
                detection_value = json.loads(textmoderation(messages, account, client_ip))

                if detection_value['Label'] == 'Normal':
                    # 标签为Normal，文本无异常
                    data = {
                        'msg': "文本无任何异常",
                        'code': 2000
                    }
                    return SuccessResponse(data=data)
                
                try:
                    # 将违禁文本存储到数据库中
                    TextDetection.objects.create(account=account, account_ip=client_ip, text_value=messages_data, text_keyword=detection_value['Keywords'])
                except Exception as e:
                    logger.error("违禁词文本插入异常错误:%s" % (str(e)))
                    return ErrorResponse()
                    
                # 判断是邮箱还是open_id
                filter_condition = Q(email=account) if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', account) else Q(open_id=account)
                
                if detection_value['Suggestion'] == 'Block':
                    # 严重违禁情况下次数+2
                    Users.objects.filter(filter_condition).update(
                        detection_counts=Case(
                            When(detection_counts__isnull=True, then=Value(2)),
                            default=F('detection_counts') + 2,
                            output_field=IntegerField(),
                        )
                    )
                    data = {
                        'msg': "请不要输入敏感词，多次警告无效后将会封禁账号！",
                        'code': 2004
                    }
                else:
                    # 普通违禁情况下次数+1
                    Users.objects.filter(filter_condition).update(
                        detection_counts=Case(
                            When(detection_counts__isnull=True, then=Value(1)),
                            default=F('detection_counts') + 1,
                            output_field=IntegerField(),
                        )
                    )
                    data = {
                        'msg': "你的输入已经在违禁的边缘，请重新输入~",
                        'code': 2004
                    }
                    
                return SuccessResponse(data=data)
                
            except Exception as e:
                logger.error("腾讯云文本校验异常错误:%s" % (str(e)))
                return ErrorResponse()
        
        except Exception as e:
            logger.error("参数获取异常错误:%s" % (str(e)))
            return ErrorResponse(msg="文本校验出现异常，请联系管理员获取奖励~")
