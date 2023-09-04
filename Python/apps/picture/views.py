# -*- coding: utf-8 -*-
import logging

from utils.jsonResponse import SuccessResponse, ErrorResponse, DetailResponse
from system.models import StableDiffusionConfig
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

class SdModelSelectView(APIView):
    """
    查询sd绘图的模型
    """
    authentication_classes = []

    @staticmethod
    def get(self, *args, **kwargs):

        resdata = []

        try:
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
