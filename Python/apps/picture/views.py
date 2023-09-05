# -*- coding: utf-8 -*-
import logging
import datetime

from utils.jsonResponse import SuccessResponse, ErrorResponse, DetailResponse
from system.models import Users, StableDiffusionConfig
from rest_framework.views import APIView
from system.views import UserTokenCheckView
from utils.common import REGEX_MOBILE, get_parameter_dic, ast_convert

logger = logging.getLogger(__name__)


class SdModelSelectView(APIView):
    """
    查询sd绘图的模型
    """
    authentication_classes = []

    def get(self, request, *args, **kwargs):

        payload = UserTokenCheckView.token_check(request)
        if not payload:
            return ErrorResponse(msg='token校验失败，请不要模拟接口使用')

        prompt = get_parameter_dic(request).get('prompt', None)

        resdata = []

        try:
            if prompt:
                data_list = StableDiffusionConfig.objects.filter(text_name__icontains=prompt)
            else:
                # 数据不多暂时直接获取全部了
                data_list = StableDiffusionConfig.objects.all()
            resdata = [
                {
                    'sd_id': item.sd_id,
                    'model_name': item.model_name,
                    'text_name': item.text_name,
                    'is_selected': item.is_selected,
                    'created_time': item.created_time,
                    'update_time': item.update_time
                }
                for item in data_list
            ]
            return DetailResponse(data=resdata)
        except Exception as e:
            logger.error("sd绘图模型获取数据异常:%s" % (str(e)))
            return ErrorResponse(code=2004)


class SdModelCurdView(APIView):
    """
    增删改sd绘图的模型
    """
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        # 获取当前时间
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # 检查用户身份
        payload = UserTokenCheckView.token_check(request)
        if not payload:
            return ErrorResponse(msg='token校验失败，请不要模拟接口使用')

        try:
            # 获取用户的信息
            parameter_dic = get_parameter_dic(request)
            email_account = parameter_dic['user']
            curd_type = parameter_dic['curd_type']
            data = parameter_dic['data']

            # 判断用户权限
            user = Users.objects.filter(email=email_account).values('type').first()
            if user:
                user_type = user['type']
                if user_type == 'ADMIN':
                    try:
                        if curd_type == 'add':
                            StableDiffusionConfig.objects.create(text_name=data.get('textName'), model_name=data.get('modelName'), is_selected=data.get('isSelected'), created_time=now_time, update_time=now_time)
                        elif curd_type == 'del':
                            StableDiffusionConfig.objects.filter(sd_id=data).delete()
                    except Exception as e:
                            logger.error(f"请求失败: {e}")
                    return SuccessResponse()
        except Exception as e:
            logger.error(f"请求失败: {e}")
            return ErrorResponse()
